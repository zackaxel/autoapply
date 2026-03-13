"""
email_sender.py - Sends a daily digest email with new job listings.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURE THESE ---
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"   # Use a Gmail App Password, not your real password
RECIPIENT_EMAIL = "your_email@gmail.com"
# -----------------------


def send_digest(jobs: list[dict]):
    """Sends an HTML email listing all new jobs."""
    subject = f"AutoApply: {len(jobs)} New Remote Jobs Today"
    body = _build_email_body(jobs)

    # MIMEMultipart lets us send both plain text and HTML versions
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = SENDER_EMAIL
    message["To"] = RECIPIENT_EMAIL
    message.attach(MIMEText(body, "html"))

    try:
        # Connect to Gmail's SMTP server with SSL encryption
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, message.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


def _build_email_body(jobs: list[dict]) -> str:
    """Builds a clean HTML email body from the job list."""
    rows = ""
    for job in jobs:
        rows += f"""
        <tr>
            <td style="padding: 8px; border-bottom: 1px solid #eee;">{job['title']}</td>
            <td style="padding: 8px; border-bottom: 1px solid #eee;">{job['company']}</td>
            <td style="padding: 8px; border-bottom: 1px solid #eee;">{job['source']}</td>
            <td style="padding: 8px; border-bottom: 1px solid #eee;">
                <a href="{job['url']}">Apply</a>
            </td>
        </tr>
        """
    return f"""
    <html><body>
    <h2>Your Daily Remote Job Digest</h2>
    <table style="border-collapse: collapse; width: 100%;">
        <tr style="background: #1F4E79; color: white;">
            <th style="padding: 10px;">Title</th>
            <th style="padding: 10px;">Company</th>
            <th style="padding: 10px;">Source</th>
            <th style="padding: 10px;">Link</th>
        </tr>
        {rows}
    </table>
    </body></html>
    """
