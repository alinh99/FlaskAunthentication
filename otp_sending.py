import random
from datetime import datetime, timedelta
from database import User
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = os.environ.get("SMTP_SERVER", "")
PORT = os.environ.get("PORT", 0)
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "")   
PASSWORD = os.environ.get("PASSWORD", "")

def generate_otp():
    return random.randrange(100000, 999999)

def expire_time():
    return datetime.now() + timedelta(minutes=30)

def expire_time_convert_to_hour():
    time = int((expire_time() - datetime.now()).total_seconds() / 3600)
    return time

def get_user_id():
    user_id = User.query.first()
    return user_id

def get_email_by_user_id():
    user_id = get_user_id()
    email = user_id.email
    return email

def get_name_by_user_id():
    user_id = get_user_id()
    full_name = user_id.last_name + user_id.first_name
    return full_name

otp = generate_otp()
expired_in = expire_time()

def email_template():
    full_name = get_name_by_user_id()
    hour = expire_time_convert_to_hour()
    message = f"""\
        <html>
            <head></head>
            <body>
                <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
                <div style="margin:50px auto;width:70%;padding:20px 0">
                    <div style="border-bottom:1px solid #eee">
                        <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">NHl's Flask</a>
                    </div>
                    <p style="font-size:1.1em">Hi, {full_name}</p>
                    <p>Thank you for choosing NHL's Flask. Use the following OTP to complete your Sign Up procedures. OTP is valid for {hour} hours</p>
                    <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{otp}</h2>
                    <p style="font-size:0.9em;">Regards,<br />NHL's Flask</p>
                    <hr style="border:none;border-top:1px solid #eee" />
                    <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
                        <p>NHL's Flask</p>
                        <p>Danang, Vietnam</p>
                    </div>
                </div>
                </div>
            </body>
        </html>
    """
    return message

def send_email():
    recepient_email = get_email_by_user_id()
    
    mail=smtplib.SMTP(SMTP_SERVER, PORT)
    msg = MIMEMultipart('alternative')
    msg["Subject"] = "OTP for NHL's Flask"
    
    mail.ehlo()
    mail.starttls()
    mail.login(SENDER_EMAIL, PASSWORD)

    message = MIMEText(email_template(), 'html')
    msg.attach(message)
    mail.sendmail(SENDER_EMAIL, recepient_email, msg.as_string())
    mail.close()