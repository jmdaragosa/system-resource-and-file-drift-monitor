#!/usr/bin/env python3

import psutil
import json
from datetime import datetime
import time
import os

def collect_metrics():
	cpu = psutil.cpu_percent(interval=1)
	memory = psutil.virtual_memory().percent
	disk = psutil.disk_usage("/").percent

	alerts = []

	if cpu > 80:
		alerts.append("High CPU usage")
	if memory > 85:
		alerts.append("High memory usage")
	if disk > 90:
		alerts.append("Disk almost full")
	
	if not alerts:
		alerts.append("Everything ok.")
	
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
		print(data)

		with open("metrics.json", "a") as file:
			file.write(json.dumps(data) + "\n")
		time.sleep(10)
