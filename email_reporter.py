import smtplib, os
from datetime import datetime
from email.mime.text import MIMEText

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

# Report summary
summary = f"""
📊 Superbot AI Status – {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC

✅ Models trained: {len(os.listdir('../models'))}
📂 Logs recorded: {len(os.listdir('../logs'))}
🕒 Next learn run in 10 minutes; other tasks hourly/daily
"""

msg = MIMEText(summary)
msg['Subject'] = "🧠 Superbot Status Report"
msg['From'] = EMAIL_FROM
msg['To'] = EMAIL_TO

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        print(f"✅ Email sent to {EMAIL_TO}")
except Exception as e:
    print(f"❌ Email failed: {e}")
