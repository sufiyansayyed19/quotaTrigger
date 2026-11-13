import os
import sys
import time
import smtplib
import configparser
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from quota_fetcher import get_quota_summary, format_quota_report
from template import build_html_email

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.ini")

def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Config file not found at: {CONFIG_FILE}")
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding="utf-8")
    return config

def send_notification_email(subject=None, body_content=None):
    config = load_config()
    sender = config.get("email", "sender_email").strip('"')
    password = config.get("email", "app_password").strip('"').replace(" ", "")
    recipient = config.get("email", "recipient_email").strip('"')
    smtp_server = config.get("email", "smtp_server", fallback="smtp.gmail.com").strip('"')
    smtp_port = config.getint("email", "smtp_port", fallback=587)

    if password == "YOUR_16_DIGIT_APP_PASSWORD_HERE":
        print("[ERROR] Please replace YOUR_16_DIGIT_APP_PASSWORD_HERE with your real App Password in config.ini!")
        return False

    now_str = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    if not subject:
        subject = f"🚀 Antigravity Quota Refreshed! ({now_str})"

    groups, plan_name, ts_str = get_quota_summary()
    plain_text = body_content if body_content else format_quota_report(groups, plan_name, ts_str)
    html_content = build_html_email(groups, plan_name, ts_str)

    msg = MIMEMultipart("alternative")
    msg["From"] = f"Antigravity Monitor <{sender}>"
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(plain_text, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    try:
        print(f"Connecting to {smtp_server}:{smtp_port}...")
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=15)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print(f"[{now_str}] Notification email successfully sent to {recipient}")
        return True
    except Exception as e:
        print(f"[{now_str}] Failed to send email: {e}")
        return False

if __name__ == "__main__":
    print("Testing email notification with live quota report...")
    success = send_notification_email()
    if success:
        print("Test passed!")
    else:
        print("Test failed. Check your config.ini credentials.")
