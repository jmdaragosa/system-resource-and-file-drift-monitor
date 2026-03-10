#!/usr/bin/env python3

import psutil
import json
from datetime import datetime
import time
import os
from anomaly_detection import make_history, detect_anomaly

WATCH_PATHS = [
	"/Users/jmdaragosa/Documents/EduCLaaS_files",
	"/Users/jmdaragosa/Downloads"
]

# Fixed threshold
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 85
DISK_THRESHOLD = 90
FILE_GROWTH_THRESHOLD_MB = 500

# Store previous directory snapshots
previous_snapshots = {}

# Rolling histories for system metrics (for anomaly detection)
cpu_history = make_history()
memory_history = make_history()
disk_history = make_history()

# Rolling histories for directory growth per path
growth_histories = {}


def scan_directory(path):
	total_size = 0
	file_count = 0

	for root, _, files in os.walk(path):
		for f in files:
			fp = os.path.join(root, f)
			try:			
				total_size += os.path.getsize(fp)
				file_count += 1
			except FileNotFoundError:
				# In case the file is deleted while scanning
				pass
	return{
		"path": path,
		"total_size_mb": round(total_size / (1024 * 1024), 2),
		"file_count": file_count
	}


def check_file_drift():
	alerts = []

	drift_info = {}

	for path in WATCH_PATHS:
		snapshot = scan_directory(path)
		current_size = snapshot["total_size_mb"]

		# Get previous size; if none, use current as baseline
		prev_size = previous_snapshots.get(
			path,
			{"total_size_mb": current_size}
		)["total_size_mb"]

		growth_mb = current_size - prev_size

		if growth_mb > FILE_GROWTH_THRESHOLD_MB:
			alerts.append(
				f"{path} grew more than {FILE_GROWTH_THRESHOLD_MB}MB"
			)
		
		if path not in growth_histories:
			growth_histories[path] = make_history()
		
		is_anom_growth, z_growth = detect_anomaly(
			growth_mb,
			growth_histories[path]
		)

		if is_anom_growth and growth_mb > 0:
			alerts.append(
				f"Anomalous growth in {path}: "
				f"+{growth_mb:.2f}MB vs recent baseline (z={z_growth:.2f})"
			)

		# Update previous_snapshots for next loop
		previous_snapshots[path] = {
			"timestamp": datetime.now().isoformat,
			"total_size_mb": current_size,
			"file_count": snapshot['file_count']
		}

		# Save info for display/logging
		drift_info[path] = {
			"total_size_mb": current_size,
			"file_count": snapshot["file_count"],
			"growth_mb": round(growth_mb, 2),
			"anomaly_growth": {
				"is_anomaly": is_anom_growth,
				"z": round(z_growth, 3)
			}
		}

	return alerts, drift_info


def collect_metrics():
	# System metrics
	cpu = psutil.cpu_percent(interval=1)
	memory = psutil.virtual_memory().percent
	disk = psutil.disk_usage("/").percent

	# Alerts
	alerts = []

	if cpu > CPU_THRESHOLD:
		alerts.append("High CPU usage")
	if memory > MEMORY_THRESHOLD:
		alerts.append("High memory usage")
	if disk > DISK_THRESHOLD:
		alerts.append("Disk almost full")

	cpu_anom, cpu_z = detect_anomaly(cpu, cpu_history)
	memory_anom, memory_z = detect_anomaly(memory, memory_history)
	disk_anom, disk_z = detect_anomaly(disk, disk_history)

	if cpu_anom:
		alerts.append(f"Anomalous CPU usage vs baseline (z={cpu_z:.2f})")
	if memory_anom:
		alerts.append(f"Anomalous memory usage vs baseline (z={memory_z:.2f})")
	if disk_anom:
		alerts.append(f"Anomalous disk usage vs baseline (z={disk_z:.2f})")

	file_drift_alerts, drift_info = check_file_drift()
	alerts.extend(file_drift_alerts)

	if not alerts:
		alerts.append("Everything OK.")

	return{
		"timestamp": datetime.now().isoformat(),
		"cpu_percentage": cpu,
		"memory_percentage": memory,
		"disk_percentage": disk,
		"anomalies": {
			"cpu": {"is_anomaly": cpu_anom, "z": round(cpu_z, 3)},
			"memory": {"is_anomaly": memory_anom, "z": round(memory_z, 3)},
			"disk": {"is_anomaly": disk_anom, "z": round(disk_z, 3)},
		},
		"alerts": alerts,
		"drift_info": drift_info
	}


if __name__ == "__main__":
	try:
		while True:
			data = collect_metrics()
			os.system('clear')

			alerts = data["alerts"]

			print("System Metrics and Anomalies:")
			print(json.dumps({
				"timestamp": data["timestamp"],
				"cpu_percentage": data["cpu_percentage"],
				"memory_percentage": data["memory_percentage"],
				"disk_percentage": data["disk_percentage"],
				"anomalies": data["anomalies"]
			}, indent=2))

			print("\nFile Snapshots and Drifts:")
			print(json.dumps(data["drift_info"], indent=2))

			print("\nAlerts:")
			for alert in alerts:
				print(f"- {alert}")
			
			# Log metrics
			metrics_entry = {
				"timestamp": data["timestamp"],
				"cpu_percentage": data["cpu_percentage"],
				"memory_percentage": data["memory_percentage"],
				"disk_percentage": data["disk_percentage"],
				"anomalies": data["anomalies"],
				"alerts": data["alerts"]
			}
			with open("metrics.json", "a") as file:
				file.write(json.dumps(metrics_entry) + "\n")

			# Log snapshots
			snapshot_entry = {
				"timestamp": datetime.now().isoformat(),
				"paths": data["drift_info"]
			}
			with open("snapshots.json", "a") as file:
				file.write(json.dumps(snapshot_entry) + "\n")

			time.sleep(5)
	except KeyboardInterrupt:
			print("\nMonitoring stopped by user. Goodbye!")