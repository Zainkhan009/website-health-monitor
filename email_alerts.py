
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def send_email(subject, message):
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("ALERT_EMAIL")

    if not sender or not password or not receiver:
        print("Email settings missing! Check your .env file.")
        return False

    email = EmailMessage()
    email["Subject"] = subject
    email["From"] = sender
    email["To"] = receiver
    email.set_content(message)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(email)

        print("Email sent successfully!")
        return True

    except Exception as error:
        print(f"Email sending failed: {error}")
        return False


if __name__ == "__main__":
    send_email(
        "Website Monitor Test",
        "Congratulations! Your Website Health Monitor email alerts are working."
    )
