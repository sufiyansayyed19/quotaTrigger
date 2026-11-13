import os
import sys
import json
import urllib.request
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_ENV = os.path.join(SCRIPT_DIR, ".session.env")

def get_session_credentials():
    token = os.environ.get("ANTIGRAVITY_CSRF_TOKEN")
    addr = os.environ.get("ANTIGRAVITY_LS_ADDRESS")

    if not token or not addr:
        if os.path.exists(SESSION_ENV):
            with open(SESSION_ENV, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("ANTIGRAVITY_CSRF_TOKEN="):
                        token = line.strip().split("=", 1)[1]
                    elif line.startswith("ANTIGRAVITY_LS_ADDRESS="):
                        addr = line.strip().split("=", 1)[1]

    if not addr:
        addr = "localhost:62140"

    return token, addr

def fetch_quota_status():
    token, addr = get_session_credentials()
    if not token:
        return None

    url = f"http://{addr}/exa.language_server_pb.LanguageServerService/GetUserStatus"
    headers = {
        "Content-Type": "application/json",
        "Connect-Protocol-Version": "1",
        "X-Codeium-Csrf-Token": token,
    }

    try:
        req = urllib.request.Request(url, data=b"{}", headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data
    except Exception:
        # Fallback probe on port 62139 via https
        try:
            import ssl
            ctx = ssl._create_unverified_context()
            alt_url = "https://127.0.0.1:62139/exa.language_server_pb.LanguageServerService/GetUserStatus"
            req2 = urllib.request.Request(alt_url, data=b"{}", headers=headers)
            with urllib.request.urlopen(req2, context=ctx, timeout=5) as resp2:
                return json.loads(resp2.read().decode("utf-8"))
        except Exception:
            return None

def convert_utc_to_local_str(iso_utc_str):
    if not iso_utc_str or iso_utc_str == "N/A":
        return "N/A"
    try:
        # e.g. 2026-11-15T16:53:37Z
        clean_str = iso_utc_str.replace("Z", "+00:00")
        dt_utc = datetime.fromisoformat(clean_str)
        dt_local = dt_utc.astimezone()
        return dt_local.strftime("%d %b %Y, %I:%M %p")
    except Exception:
        return iso_utc_str

def get_quota_summary():
    raw_data = fetch_quota_status()
    if not raw_data:
        return {}, "Pro", datetime.now().strftime("%d %b %Y, %I:%M %p")

    user_status = raw_data.get("userStatus", {})
    plan_name = user_status.get("planStatus", {}).get("planInfo", {}).get("planName", "Pro")
    configs = user_status.get("cascadeModelConfigData", {}).get("clientModelConfigs", [])

    model_groups = {}
    for c in configs:
        lbl = c.get("label", "")
        q = c.get("quotaInfo")
        if not q or not lbl:
            continue
        base_name = lbl.split(" (")[0] if " (" in lbl else lbl
        if base_name not in model_groups:
            pct = round(q.get("remainingFraction", 0) * 100, 1)
            reset_utc = q.get("resetTime", "N/A")
            reset_local = convert_utc_to_local_str(reset_utc)
            model_groups[base_name] = {"pct": pct, "reset": reset_local}

    timestamp_str = datetime.now().strftime("%d %b %Y, %I:%M %p")
    return model_groups, plan_name, timestamp_str

def format_quota_report(model_groups, plan_name, timestamp_str):
    if not model_groups:
        return "Unable to fetch live model quota metrics from local service."

    lines = [
        f"Plan Tier: {plan_name}",
        f"Generated At: {timestamp_str} (IST)",
        "",
        "Model Quotas & Headroom:",
        "--------------------------------------------------------------------------------"
    ]
    for model_name, info in model_groups.items():
        pct = info["pct"]
        reset = info["reset"]
        bar = ("█" * int(pct // 10)).ljust(10, "░")
        lines.append(f"  • {model_name:<20} : {pct:>5.1f}% [{bar}]  (Reset: {reset})")

    lines.append("--------------------------------------------------------------------------------")
    return "\n".join(lines)

if __name__ == "__main__":
    groups, plan, ts = get_quota_summary()
    print(format_quota_report(groups, plan, ts))
