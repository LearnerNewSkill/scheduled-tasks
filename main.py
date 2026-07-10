import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# 1. Server Configuration Setup
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # Standard port for TLS encryption
SENDER_EMAIL = os.getenv("MY_EMAIL")
# ⚠️ WARNING: This must be an "App Password", NOT your regular login password!
SENDER_PASSWORD = os.getenv("MY_PASSWORD")


RECIPIENT_EMAIL = "sunilk.ug18.me@nitp.ac.in"

# 2. Construct the Email Message
message = MIMEMultipart()
message["From"] = SENDER_EMAIL
message["To"] = RECIPIENT_EMAIL
message["Subject"] = "Automated Data Alert Pipeline"

body = "The processing pipeline executed successfully. All metrics logged."
message.attach(MIMEText(body, "plain"))

#3. Securely Connect and Send (Using Exception Handling)
try:
    # Initialize the server instance
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()  # Encrypt the connection layer securely
    
    # Login and dispatch email
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(message)
    print("Email sent successfully!")

except Exception as e:
    print(f"Failed to send email. Error details: {e}")

finally:
    # Ensure the connection closes cleanly no matter what happens
    try:
        server.quit()
    except NameError:
        pass
