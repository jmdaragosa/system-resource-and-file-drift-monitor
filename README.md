# system-resource-and-file-drift-monitor
A beginner-friendly Python tool that monitors your system’s health and tracks important files, detecting anomalies automatically. It helps you understand CPU, memory, disk usage, and file changes over time.

The system performs threshold-based anomaly detection for system resources and monitored directories, generating alerts when usage exceeds configured limits or when file growth exceeds expected bounds. 

## Features
	•	System Metrics Monitoring
  Tracks CPU, memory, and disk usage on macOS, logging metrics to metrics.json.

	•	File Drift Tracking
  Monitors selected directories for file growth and unexpected modifications. Alerts   when folders grow rapidly.
  
	•	Anomaly Detection / Alerts
  Flags unusual conditions (e.g., high CPU usage, low memory, disk almost full,   files growing too fast) and prints alerts in real time.

	•	Failure / Issue Isolation
  Stores timestamped snapshots of folder sizes in snapshots.json to pinpoint when and where a problem started.

	•	Logging & Observability
  Saves structured JSON logs for easy analysis, providing a foundation for dashboards, alerts, and advanced monitoring.

	•	Live Terminal Updates & Graceful Exit
  Refreshes metrics every 5 seconds in the terminal and exits cleanly on Ctrl+C.

## Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/system-resource-and-file-drift-monitor.git
   cd system-resource-and-file-drift-monitor
2. Install dependencies
   ```bash
   pip install psutil
3. Run on monitor:
   ```bash
   ./monitor.py
   
## Configuration

	•	WATCH_PATHS: List of directories to monitor
	•	CPU_THRESHOLD, MEMORY_THRESHOLD, DISK_THRESHOLD: System alert thresholds
	•	FILE_GROWTH_THRESHOLD_MB: File growth threshold in MB

Adjust these variables at the top of monitor.py as needed.

## Future Improvements

	•	Add notifications (email or desktop) when thresholds are exceeded
	•	Visualize metrics with dashboards (Plotly, Grafana)
	•	Make thresholds and paths configurable via an external config file
	•	Support Windows/Linux
  
