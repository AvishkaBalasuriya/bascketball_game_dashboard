from django.core.mail import EmailMessage
import random


def send_email(subject, message, sent_by, to):
    try:
        msg = EmailMessage(subject, message, sent_by, [to])
        result = msg.send()
        return True
    except Exception as e:
        return False


def generate_otp_code():
    return random.randint(100000, 999999)
