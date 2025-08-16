import random
import smtplib
import os
import time
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models import User, Child

load_dotenv("prod.env")

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Storage: email -> (otp, timestamp)
otp_store = {}
verified_emails = set()

def generate_otp(length=6):
    return str(random.randint(10**(length - 1), 10**length - 1))

def send_otp_email(receiver_email, otp):
    subject = "Your OTP for email verification"
    body = f"Your OTP is: {otp}\nIt is valid for 90 seconds."

    msg = MIMEMultipart()
    msg['From'] = SMTP_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, receiver_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Failed to send email:", e)
        return False

def store_otp(email):
    otp = generate_otp()
    timestamp = time.time()
    otp_store[email] = (otp, timestamp)
    sent = send_otp_email(email, otp)
    return sent

def verify_otp(email, input_otp):
    if email not in otp_store:
        return False, "OTP not requested for this email."  
    stored_otp, timestamp = otp_store[email]
    print(stored_otp)
    current_time = time.time()
    if current_time - timestamp > 90:
        del otp_store[email]
        return False, "OTP has expired."
    if input_otp == (stored_otp):
        del otp_store[email]
        verified_emails.add(email)
        return True, "OTP verified successfully."
    return False, "Incorrect OTP."

def send_welcome_email(email, user_id):
    subject = "Welcome to Our App - Complete Your Profile"
    msg = MIMEMultipart()
    msg['From'] = SMTP_EMAIL
    msg['To'] = email
    msg['Subject'] = subject

    body = f"""
    <h3>Welcome to Our Platform!</h3>
    <p>Hi there ,</p>
    <p>Your Google account was successfully registered.</p>

    <p>To complete your profile, log in and visit your profile page</a>.</p>
    <p>If you forgot username or password, you can use our forgot username and forgot password option in Login page.</p>

    <br>
    <p>Thanks & Regards,<br>Team Slice</p>
    """

    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
            smtp.send_message(msg)
        print(f"Email sent to {email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_mail_username(email, username):
    subject = "Your Username Information"
    msg = MIMEMultipart()
    msg['From'] = SMTP_EMAIL
    msg['To'] = email
    msg['Subject'] = subject

    body = f"""
    <html>
        <body>
            <h3>Welcome to Our Platform!</h3>
            <p>Hi there,</p>
            <p><strong>Your username is:</strong> <code>{username}</code></p>
            <br>
            <p>Thanks & Regards,<br>Team Slice</p>
        </body>
    </html>
    """

    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
            smtp.send_message(msg)
        print(f"Email sent to {email}")
    except Exception as e:
        print(f"Failed to send email: {e}")


def send_child_credentials_email(username, password, child_name, email):
    subject = f"Account Details for Your Child - {child_name}"
    msg = MIMEMultipart()
    msg['From'] = SMTP_EMAIL
    msg['To'] = email
    msg['Subject'] = subject

    body = f"""
    <html>
        <body>
            <h3>Child Account Created Successfully!</h3>
            <p>Hello,</p>
            <p>The account for your child <strong>{child_name}</strong> has been successfully created.</p>
            <p><strong>Username:</strong> <code>{username}</code></p>
            <p><strong>Password:</strong> <code>{password}</code></p>
            <p>Please keep these credentials safe.</p>
            <br>
            <p>Thanks & Regards,<br>Team Slice</p>
        </body>
    </html>
    """

    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
            smtp.send_message(msg)
        print(f"Child credentials email sent to {email}")
    except Exception as e:
        print(f"Failed to send child credentials email: {e}")


otp_store_username = {}
verified_usernames = set()

def send_child_otp_email(receiver_email, child_name, otp):
    subject = f"Your OTP for {child_name} account verification"
    body = f"Your child {child_name} account otp: {otp}"

    msg = MIMEMultipart()
    msg['From'] = SMTP_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, receiver_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Failed to send email:", e)
        return False
    
def store_child_otp(username):
    otp = generate_otp()
    timestamp = time.time()
    otp_store_username[username] = (otp, timestamp)
    user = User.query.filter_by(username=username, role="child").first()
    if not user:
        return False
    email = user.email
    child = Child.query.filter_by(user_id=user.id).first()
    sent = send_child_otp_email(email, child.name, otp)
    return sent

def verify_otp_username(username, input_otp):
    if username not in otp_store_username:
        return False, "OTP not requested for this username."  
    stored_otp, timestamp = otp_store_username[username]
    current_time = time.time()
    if current_time - timestamp > 90:
        del otp_store_username[username]
        return False, "OTP has expired."
    if str(input_otp) == str(stored_otp):
        del otp_store_username[username]
        verified_usernames.add(username)
        return True, "OTP verified successfully."
    return False, "Incorrect OTP."

# Resend OTP for email verification
def resend_otp(email):
    if email in otp_store:
        del otp_store[email] 
    return store_otp(email)

# Resend OTP for child account verification
def resend_child_otp(username):
    if username in otp_store_username:
        del otp_store_username[username]   
    return store_child_otp(username)
# Resend OTP for parent register account verification



