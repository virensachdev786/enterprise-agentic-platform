import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration - Use Environment Variables in Production!
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "veebee@veeren.co"
SENDER_PASSWORD = "APP PASSWORD"

def send_external_email(recipient_email: str, subject: str, body: str):
    """
    Sends a physical email via SMTP.
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Connect and Send
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return {"status": "success", "details": f"Email sent to {recipient_email}"}
    except Exception as e:
        print(f"SMTP Error: {e}")
        return {"status": "failed", "error": str(e)}