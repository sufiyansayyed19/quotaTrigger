import sys
import time
from datetime import datetime, timedelta
from notifier import send_notification_email

def schedule_trigger(hours=5.0):
    now = datetime.now()
    trigger_time = now + timedelta(hours=hours)
    
    print(f"==================================================")
    print(f" Antigravity 5-Hour Rolling Refresh Timer")
    print(f" Scheduled at : {now.strftime('%Y-%m-%d %I:%M:%S %p')}")
    print(f" Target time  : {trigger_time.strftime('%Y-%m-%d %I:%M:%S %p')}")
    print(f" Waiting      : {hours:.1f} hours...")
    print(f"==================================================")
    
    seconds_to_wait = int(hours * 3600)
    time.sleep(seconds_to_wait)
    
    print("Timer finished! Sending refresh email notification...")
    send_notification_email(
        subject="🚀 Antigravity 5-Hour Quota Refresh Reached!",
        body_content=(
            f"Hello Sufiyan,\n\n"
            f"Your 5-hour rolling refresh interval has passed.\n"
            f"Timestamp: {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}\n\n"
            f"Your tokens have replenished from your previous session.\n\n"
            f"— Antigravity Quota Timer"
        )
    )

if __name__ == "__main__":
    delay_hours = 5.0
    if len(sys.argv) > 1:
        try:
            delay_hours = float(sys.argv[1])
        except ValueError:
            pass
    schedule_trigger(delay_hours)
