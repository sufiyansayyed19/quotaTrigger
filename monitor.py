import os
import sys
import time
import glob
from datetime import datetime, timedelta
from notifier import send_notification_email, load_config

GEMINI_LOG_DIR = os.path.expanduser(r"~\.gemini\antigravity-cli\log")

def get_latest_log_file():
    pattern = os.path.join(GEMINI_LOG_DIR, "cli-*.log")
    matches = glob.glob(pattern)
    if not matches:
        # Fallback to general cli.log
        fallback = os.path.expanduser(r"~\.gemini\antigravity-cli\cli.log")
        return fallback if os.path.exists(fallback) else None
    return max(matches, key=os.path.getmtime)

def run_monitor():
    config = load_config()
    poll_sec = config.getint("monitor", "poll_interval_seconds", fallback=60)
    cooldown_min = config.getint("monitor", "cooldown_minutes", fallback=240)
    cooldown_delta = timedelta(minutes=cooldown_min)

    last_notified = None
    log_file = get_latest_log_file()

    print(f"==================================================")
    print(f" Antigravity Quota Refresh Daemon Started")
    print(f" Target Log: {log_file}")
    print(f" Poll Interval: {poll_sec}s | Cooldown: {cooldown_min}m")
    print(f"==================================================")

    if not log_file or not os.path.exists(log_file):
        print(f"[WARNING] Log file not found yet. Waiting for Antigravity activity...")

    file_pos = 0
    if log_file and os.path.exists(log_file):
        file_pos = os.path.getsize(log_file)

    while True:
        try:
            current_log = get_latest_log_file()
            if current_log != log_file:
                print(f"[INFO] Active log file rotated: {current_log}")
                log_file = current_log
                file_pos = 0

            if log_file and os.path.exists(log_file):
                current_size = os.path.getsize(log_file)
                if current_size < file_pos:
                    # File truncated or reset
                    file_pos = 0

                if current_size > file_pos:
                    with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                        f.seek(file_pos)
                        new_lines = f.readlines()
                        file_pos = f.tell()

                        for line in new_lines:
                            # Detect quota reload events from quota_manager.go
                            if "quota_manager.go" in line and "doRefreshQuota: starting reload" in line:
                                now = datetime.now()
                                print(f"[{now.strftime('%H:%M:%S')}] Detected quota reload event in log!")
                                
                                # Check cooldown
                                if last_notified is None or (now - last_notified) >= cooldown_delta:
                                    print("Sending email notification...")
                                    sent = send_notification_email()
                                    if sent:
                                        last_notified = now
                                else:
                                    elapsed = (now - last_notified).total_seconds() / 60
                                    print(f"[Cooldown] Refresh event detected but email suppressed ({elapsed:.1f}m / {cooldown_min}m elapsed).")

            time.sleep(poll_sec)

        except KeyboardInterrupt:
            print("\nMonitor stopped by user.")
            break
        except Exception as e:
            print(f"[ERROR] Exception during polling: {e}")
            time.sleep(poll_sec)

if __name__ == "__main__":
    run_monitor()
