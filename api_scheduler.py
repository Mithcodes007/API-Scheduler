#!/usr/bin/env python3
"""
api_scheduler.py

Schedule API calls to ifconfig.co at precise timestamps (HH:MM:SS).
If multiple timestamps match the same second, they run in parallel threads.
"""

import argparse
import datetime
import logging
import threading
import time
import urllib.request
import urllib.error
import urllib.parse
import sys
import os
from typing import List, Dict

# Global config
API_URL = os.environ.get("API_URL", "https://ifconfig.co/json")

def configure_logger(log_file: str = "api_scheduler.log") -> logging.Logger:
    logger = logging.getLogger("api_scheduler")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fmt = logging.Formatter("%(asctime)s: %(message)s", "%Y-%m-%d %H:%M:%S")
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(fmt)
        fh = logging.FileHandler(log_file)
        fh.setFormatter(fmt)
        logger.addHandler(sh)
        logger.addHandler(fh)
    return logger

def parse_timestamps(ts_input: str) -> List[datetime.time]:
    parts = [p.strip() for p in ts_input.replace("\n", ",").split(",") if p.strip()]
    times = []
    for p in parts:
        try:
            times.append(datetime.datetime.strptime(p, "%H:%M:%S").time())
        except ValueError:
            raise ValueError(f"Invalid timestamp format: '{p}'. Expected HH:MM:SS")
    return times

def build_schedule(times: List[datetime.time],
                   base_date: datetime.date = None,
                   run_missed: bool = False,
                   logger: logging.Logger = None) -> Dict[datetime.datetime, List[int]]:
    if base_date is None:
        base_date = datetime.date.today()
    now = datetime.datetime.now()
    schedule = {}
    for idx, t in enumerate(times):
        dt = datetime.datetime.combine(base_date, t)
        if dt < now:
            if run_missed:
                dt = now + datetime.timedelta(seconds=1)
            else:
                if logger:
                    logger.warning(f"Skipping past timestamp {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                continue
        schedule.setdefault(dt, []).append(idx)
    return schedule

def call_api(api_url: str, logger: logging.Logger, idx: int, timeout: int = 10) -> bool:
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": "API-Scheduler/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if 200 <= resp.getcode() < 400:
                logger.info(f"Successfully called API at {urllib.parse.urlparse(api_url).netloc}")
                return True
            else:
                logger.error(f"API returned status {resp.getcode()}")
                return False
    except urllib.error.HTTPError as e:
        logger.error(f"HTTPError: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        logger.error(f"URLError: {e.reason}")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
    return False

def wait_and_dispatch(schedule: Dict[datetime.datetime, List[int]],
                      api_url: str,
                      logger: logging.Logger):
    if not schedule:
        logger.info("No timestamps to schedule. Exiting.")
        return
    times = sorted(schedule.keys())
    for scheduled_time in times:
        now = datetime.datetime.now()
        delta = (scheduled_time - now).total_seconds()
        if delta > 0:
            time.sleep(delta)
        logger.info(f"{scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}: Dispatching {len(schedule[scheduled_time])} call(s).")
        for idx in schedule[scheduled_time]:
            t = threading.Thread(target=call_api, args=(api_url, logger, idx))
            t.daemon = True
            t.start()
    logger.info("All dispatches triggered.")

def main():
    parser = argparse.ArgumentParser(description="Schedule API calls to ifconfig.co")
    parser.add_argument("timestamps", nargs="?", help='e.g. "09:15:25,11:58:23"')
    parser.add_argument("--file", "-f", help="File with timestamps (comma/newline separated)")
    parser.add_argument("--log-file", default="api_scheduler.log")
    parser.add_argument("--run-missed", action="store_true", help="Run past timestamps immediately")
    parser.add_argument("--dry-run", action="store_true", help="Show schedule without dispatching")
    args = parser.parse_args()

    logger = configure_logger(args.log_file)

    raw_ts = ""
    if args.file:
        raw_ts = open(args.file).read()
    elif args.timestamps:
        raw_ts = args.timestamps
    else:
        logger.error("No timestamps provided.")
        parser.print_help()
        sys.exit(1)

    try:
        times = parse_timestamps(raw_ts)
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)

    schedule = build_schedule(times, run_missed=args.run_missed, logger=logger)

    if args.dry_run:
        for t, lst in sorted(schedule.items()):
            logger.info(f"{t}: {len(lst)} call(s)")
        return

    wait_and_dispatch(schedule, API_URL, logger)

if __name__ == "__main__":
    main()
