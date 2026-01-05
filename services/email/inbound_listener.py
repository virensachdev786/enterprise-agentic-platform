import imaplib
import email
from email.header import decode_header
import requests
import time
import traceback

# --- Configuration ---
IMAP_SERVER = "imap.gmail.com"
EMAIL_USER = "veebee@veeren.co"      # The Agent's email
EMAIL_PASS = "APP PASSWORD"   # App Password
BACKEND_URL = "http://localhost:8000/process_email"
AUTHORIZED_USERS = ["virens88@gmail.com"]

def clean_header(header_val):
    """Decodes email headers (Subject, From) safely."""
    if not header_val:
        return "No Subject"
    decoded = decode_header(header_val)
    header_sections = []
    for content, charset in decoded:
        if isinstance(content, bytes):
            header_sections.append(content.decode(charset or "utf-8", errors="ignore"))
        else:
            header_sections.append(str(content))
    return "".join(header_sections)

def process_latest_emails():
    """Connects to IMAP, fetches unseen mail, and sends to the backend."""
    try:
        # 1. Establish Secure Connection
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        # 2. Search for UNSEEN emails
        status, messages = mail.search(None, 'UNSEEN')
        
        if status == "OK" and messages[0]:
            # messages[0] contains a space-separated list of email IDs
            for num in messages[0].split():
                # Fetch the full email content
                _, msg_data = mail.fetch(num, '(RFC822)')
                
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Extract sender and clean it
                        raw_from = msg.get("From", "")
                        sender = email.utils.parseaddr(raw_from)[1].lower().strip()

                        # --- LOGIC GATES ---
                        
                        # A. Avoid Self-Loops
                        if sender == EMAIL_USER.lower():
                            continue

                        # B. Authorized Check
                        if sender not in [user.lower() for user in AUTHORIZED_USERS]:
                            print(f"🛑 Blocked: Unauthorized sender {sender}")
                            mail.store(num, '+FLAGS', '\\Seen') # Mark as read to ignore next time
                            continue

                        # C. Authorized - Extract Content
                        subject = clean_header(msg.get("Subject"))
                        body = ""

                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                try:
                                    if content_type == "text/plain" and "attachment" not in content_disposition:
                                        body = part.get_payload(decode=True).decode(errors="ignore")
                                        break
                                except Exception:
                                    pass
                        else:
                            body = msg.get_payload(decode=True).decode(errors="ignore")

                        # --- DISPATCH TO BACKEND ---
                        print("-" * 50)
                        print(f"📩 Authorized Request from: {sender}")
                        print(f"Subject: {subject}")
                        
                        payload = {"email": sender, "body": body}
                        
                        try:
                            # Forwarding to your FastAPI Orchestrator
                            response = requests.post(BACKEND_URL, json=payload, timeout=45)
                            if response.status_code == 200:
                                print(f"✅ Agent processed email: {response.status_code}")
                            else:
                                print(f"⚠️ Backend returned error: {response.status_code} - {response.text}")
                        except requests.exceptions.RequestException as e:
                            print(f"❌ Failed to reach Backend: {e}")

        # Logout safely
        mail.logout()

    except Exception as e:
        print(f"📡 IMAP Error: {e}")
        # traceback.print_exc() # Uncomment for deep debugging

def listen_for_emails():
    """Main loop to poll the inbox every 5 seconds."""
    print(f"🚀 Listener Active: Watching {EMAIL_USER}...")
    print(f"🔒 Lockdown Mode: Only accepting requests from {AUTHORIZED_USERS}")
    print("Press Ctrl+C to stop.")
    
    while True:
        process_latest_emails()
        time.sleep(5) # Poll every 5 seconds for a fast demo feel

if __name__ == "__main__":
    listen_for_emails()