#!/usr/bin/env python3

import psutil
import json
from datetime import datetime

def collect_metrics():
	return{
		"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
		"cpu_percentage": psutil.cpu_percent(interval=1),
		"memory_percentage": psutil.virtual_memory().percent,
		"disk_percent": psutil.disk_usage("/").percent
	}

if __name__ == "__main__":
	data = collect_metrics()
	print(data)

	with open("metrics.json", "a") as file:
		file.write(json.dumps(data) + "\n")
