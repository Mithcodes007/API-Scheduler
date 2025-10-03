# API Scheduler

Schedules API calls to `ifconfig.co` at exact times (HH:MM:SS).  
Multiple calls at the same second run in parallel threads.

## Run

Inline timestamps:
```bash
python api_scheduler.py "09:15:25,11:58:23,13:45:09"
