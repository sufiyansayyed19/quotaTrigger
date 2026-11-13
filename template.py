def build_html_email(model_groups, plan_name, timestamp_str):
    cards_html = ""
    for model_name, info in model_groups.items():
        pct = info["pct"]
        reset = info["reset"]
        
        # Color badge depending on percentage
        if pct >= 70:
            badge_color = "#10b981"  # Emerald green
            bar_color = "#10b981"
            status_text = "Healthy"
        elif pct >= 30:
            badge_color = "#f59e0b"  # Amber
            bar_color = "#f59e0b"
            status_text = "Moderate"
        else:
            badge_color = "#ef4444"  # Red
            bar_color = "#ef4444"
            status_text = "Low Quota"

        cards_html += f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px 18px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-weight: 700; color: #1e293b; font-size: 15px;">{model_name}</span>
                <span style="background-color: {badge_color}18; color: {badge_color}; font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 9999px;">
                    {status_text} • {pct}%
                </span>
            </div>
            
            <!-- Progress Bar -->
            <div style="background: #f1f5f9; border-radius: 8px; height: 10px; width: 100%; overflow: hidden; margin-bottom: 8px;">
                <div style="background: {bar_color}; height: 100%; width: {pct}%; border-radius: 8px;"></div>
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: #64748b;">
                <span>Available Headroom</span>
                <span style="color: #475569; font-weight: 500;">Reset: <strong>{reset}</strong></span>
            </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Antigravity Quota Status</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f8fafc; padding: 24px 12px;">
        <tr>
            <td align="center">
                <table role="presentation" width="100%" style="max-width: 540px; background-color: #ffffff; border-radius: 16px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
                    
                    <!-- Header -->
                    <tr>
                        <td style="padding: 24px 24px 18px 24px; background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%); color: #ffffff;">
                            <div style="display: inline-block; background: rgba(255, 255, 255, 0.2); padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                                {plan_name} Tier • Active Sync
                            </div>
                            <h1 style="margin: 0 0 6px 0; font-size: 22px; font-weight: 800; letter-spacing: -0.5px;">Antigravity Quota Reloaded</h1>
                            <p style="margin: 0; font-size: 13px; opacity: 0.9;">Refreshed at {timestamp_str}</p>
                        </td>
                    </tr>
                    
                    <!-- Content Area -->
                    <tr>
                        <td style="padding: 20px 20px 10px 20px; background-color: #f8fafc;">
                            <p style="margin: 0 0 16px 0; font-size: 13px; color: #475569; line-height: 1.5;">
                                Hi Sufiyan, here is your updated quota status and model headroom across your workspace:
                            </p>
                            
                            <!-- Cards -->
                            {cards_html}
                            
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="padding: 16px 24px; background-color: #f1f5f9; text-align: center; border-top: 1px solid #e2e8f0; font-size: 11px; color: #94a3b8;">
                            Antigravity Agent Daemon • Monitored via Local RPC
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
    """
    return html
