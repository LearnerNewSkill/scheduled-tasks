import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import requests
from datetime import datetime

MY_LAT = 25.991346
MY_LONG = 79.469125
MY_API_ID = os.getenv("MY_API_ID")
RECIPIENT_EMAIL = "sunilkumarr0202@gmail.com"
TIME_LIMIT = 6
Current_weather_end_point = "https://api.openweathermap.org/data/2.5/weather"
three_hour_end_point = "https://api.openweathermap.org/data/2.5/forecast"
parameter = {
    "lat":MY_LAT,
    "lon":MY_LONG,
    "appid":MY_API_ID,
    "cnt": TIME_LIMIT,
}

response = requests.get(url=three_hour_end_point,params=parameter)

def date_conv(dt):
    dt_object = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    formatted_time = dt_object.strftime("%I %p")
    return formatted_time

my_weather = {}

for i in response.json()["list"]:
    weather_desc = i["weather"][0]["description"]
    weather_time = date_conv(i["dt_txt"])
    my_weather[weather_time] = weather_desc

my_city = response.json()["city"]["name"]

# 1. Server Configuration Setup
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # Standard port for TLS encryption
SENDER_EMAIL = os.getenv("MY_EMAIL")
# ⚠️ WARNING: This must be an "App Password", NOT your regular login password!
SENDER_PASSWORD = os.getenv("MY_PASSWORD")


# 2. Construct the Email Message
message = MIMEMultipart()
message["From"] = SENDER_EMAIL
message["To"] = RECIPIENT_EMAIL
message["Subject"] = f"Weather Update for {datetime.today().strftime("%d %B %Y").lower()}"

weather_rows = "\n".join(f"- {time}: {details}" for time, details in my_weather.items())
body = (
    f"Hi,\n\n"
    f"Please find today's weather update for {my_city} organized by time:\n"
    f"{weather_rows}\n\n"
    f"Best Regards,\n"
    f"Weather Monitor"
)
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
