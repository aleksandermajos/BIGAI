import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ENGINE.KEY_GMAIL import provide_key

# Email configuration
sender_email = "aleksander.majos@gmail.com"
receiver_email = "aleksander.majos@gmail.com"
subject = "NEW PROMPT"
body = "hakuna"
password = provide_key()


def send_mail(body, sender_email="aleksander.majos@gmail.com", receiver_email="aleksander.majos@gmail.com", subject="NEW PROMPT"):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade to secure connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        info = "Email sent successfully!"
        print(info)
    except Exception as e:
        info = 'Failed to send email'
        print(f"Failed to send email: {e}")
    return info

send_mail(sender_email, receiver_email, subject, body)
