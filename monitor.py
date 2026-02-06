#!/usr/bin/env python3

import psutil
import json
from datetime import datetime
import time
import os

WATCH_PATHS = [
	"/Users/jmdaragosa/Documents/EduCLaaS_files",
	"/Users/jmdaragosa/Downloads"
]


CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 85
DISK_THRESHOLD = 90
FILE_GROWTH_THRESHOLD_MB = 500


previous_snapshots = {}


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

	for path in WATCH_PATHS:
		snapshot = scan_directory(path)
		prev_size = previous_snapshots.get(path, snapshot["total_size_mb"])
		if snapshot["total_size_mb"] - prev_size > FILE_GROWTH_THRESHOLD_MB:
			alerts.append(f"{path} grew more than {FILE_GROWTH_THRESHOLD_MB}MB")
		previous_snapshots[path] = snapshot["total_size_mb"]

		return alerts


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
	
	# File drift alerts
	file_drift_alerts = check_file_drift()
	alerts.extend(file_drift_alerts)

	if not alerts:
		alerts.append("Everything OK.")

	return{
		"timestamp": datetime.now().isoformat(),
		"cpu_percentage": cpu,
		"memory_percentage": memory,
		"disk_percent": disk,
		"alerts": alerts
	}





if __name__ == "__main__":
	while True:
		data = collect_metrics()
		os.system('clear')
		print(json.dumps(data, indent=2))

		with open("metrics.json", "a") as file:
			file.write(json.dumps(data) + "\n")
		time.sleep(5)
