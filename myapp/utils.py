# myapp/utils.py
from django.core.mail import EmailMessage
from django.conf import settings
import secrets
# myapp/utils.py
import re

def is_valid_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$', email)


from_email = settings.DEFAULT_FROM_EMAIL

def generate_confirmation_token():
    return secrets.token_urlsafe(32)

def send_confirmation_email(email, confirmation_token):
    subject = 'Email Confirmation for Woro Assignment(Abinash Nayak)'
    message = f'Hello,\n\nPlease use the following token to confirm your email: {confirmation_token}\n\nThank you!\nWoro Team'
    to_email = email

    email_message = EmailMessage(subject, message, from_email, [to_email])

    try:
        email_message.send()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False  
