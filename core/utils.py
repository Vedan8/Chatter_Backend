# core/utils.py

from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp}. Please use this to verify your registration.'
    from_email = settings.EMAIL_HOST_USER

    send_mail(subject, message, from_email, [email])
