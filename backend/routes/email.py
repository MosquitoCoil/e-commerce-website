from flask import Blueprint, request, redirect, flash, url_for
import smtplib
from email.mime.text import MIMEText
from datetime import date
import os

email_bp = Blueprint("email", __name__)

# Store counters in memory
daily_email_count = {"date": date.today(), "count": 0}


@email_bp.route("/send-email", methods=["POST"])
def send_email():
    global daily_email_count

    # Reset counter if new day
    if daily_email_count["date"] != date.today():
        daily_email_count = {"date": date.today(), "count": 0}

    # Limit check
    if daily_email_count["count"] >= 10:
        flash("Email limit reached. Please try again tomorrow.", "danger")
        return redirect(url_for("home.home"))

    name = request.form.get("name")
    subject = request.form.get("subject")
    sender_email = request.form.get("email")
    message_body = request.form.get("message")

    msg = MIMEText(f"Message from {name} <{sender_email}>:\n\n{message_body}")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = "jaymarroco1016@gmail.com"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("jaymarroco1016@gmail.com", os.environ.get("EMAIL_PASS"))
            server.sendmail(sender_email, "jaymarroco1016@gmail.com", msg.as_string())

        daily_email_count["count"] += 1
        flash("Your message has been sent successfully!", "success")
    except Exception as e:
        flash("Failed to send message. Please try again later.", "danger")
        print("Error:", e)

    return redirect(url_for("home.home"))
