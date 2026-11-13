# Antigravity Quota Refresh Email Trigger

This project monitors your local Antigravity quota lifecycle and sends an email to `sufiyan.sayed92@gmail.com` when your quota refreshes.

---

## 📁 Files in This Project
1. **[`config.ini`](file:///C:/Users/skamalud/OneDrive%20-%20Capgemini/Documents/Python-Project/Quota_trigger/config.ini)** - Contains email configuration and notification settings.
2. **[`notifier.py`](file:///C:/Users/skamalud/OneDrive%20-%20Capgemini/Documents/Python-Project/Quota_trigger/notifier.py)** - Core email sending engine using Gmail SMTP.
3. **[`monitor.py`](file:///C:/Users/skamalud/OneDrive%20-%20Capgemini/Documents/Python-Project/Quota_trigger/monitor.py)** - Real-time background daemon that detects `doRefreshQuota` events in Antigravity's local logs.
4. **[`timer_trigger.py`](file:///C:/Users/skamalud/OneDrive%20-%20Capgemini/Documents/Python-Project/Quota_trigger/timer_trigger.py)** - A 5-hour rolling countdown trigger (run whenever you finish a heavy session).

---

## 🔑 One-Time Setup: Generate a Google App Password
Since you are using a personal Gmail account (`sufiyan.sayed92@gmail.com`), Google requires a 16-character **App Password** for SMTP scripts:

1. Go to your **[Google Account Security](https://myaccount.google.com/security)** page.
2. Ensure **2-Step Verification** is turned ON.
3. Search for **App Passwords** (or visit: `https://myaccount.google.com/apppasswords`).
4. Enter an app name (e.g. `Antigravity Quota`) and click **Create**.
5. Copy the generated 16-character password (e.g. `abcd efgh ijkl mnop`).
6. Open **[`config.ini`](file:///C:/Users/skamalud/OneDrive%20-%20Capgemini/Documents/Python-Project/Quota_trigger/config.ini)** and paste it into `app_password`:
   ```ini
   app_password = "abcd efgh ijkl mnop"
   ```

---

## 🚀 How to Use

### 1. Test the Email Setup
Run in your PowerShell or terminal:
```powershell
python "C:\Users\skamalud\OneDrive - Capgemini\Documents\Python-Project\Quota_trigger\notifier.py"
```
You should receive a test email in `sufiyan.sayed92@gmail.com`.

### 2. Run the Real-Time Event Monitor
To listen continuously for Antigravity's quota reload events in the background:
```powershell
python "C:\Users\skamalud\OneDrive - Capgemini\Documents\Python-Project\Quota_trigger\monitor.py"
```

### 3. Or Run a 5-Hour Rolling Countdown Timer
Whenever you exhaust your quota in a heavy coding sprint and want an alert right when the 5-hour rolling window clears:
```powershell
python "C:\Users\skamalud\OneDrive - Capgemini\Documents\Python-Project\Quota_trigger\timer_trigger.py" 5
```
Or set any custom hours (e.g. `python timer_trigger.py 2.5`).
