**🕒 API Scheduler**

A lightweight Python-based scheduler to automate and log API requests at specific timestamps.
Perfect for running time-based API calls (like heartbeat checks, data syncs, or webhook testing).

**🚀 Features**

Schedule multiple API calls at custom timestamps

Supports GET and POST requests

Optional dry-run mode (test schedules without execution)

Logs every run, skip, and error with timestamps

Simple CLI interface

**⚙️ Usage**
Run the script
python api_scheduler.py "12:00:05,12:00:10,12:00:15"


This runs the scheduler for the specified times (24-hour format).

Dry run (no actual API calls)
python api_scheduler.py "12:00:05,12:00:10" --dry-run

Example log output
2025-10-03 12:00:05: Executing API request...
2025-10-03 12:00:10: Skipping past timestamp 2025-10-03 12:00:05

**🧠 How It Works**

Reads timestamps from command-line arguments

Waits until each scheduled time

Sends API requests (or simulates in dry-run)

Logs results to the console and file

**📁 Project Structure**
├── api_scheduler.py   # Main script
├── requirements.txt   # Dependencies (if any)
└── README.md          # Project documentation
