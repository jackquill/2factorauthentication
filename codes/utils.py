from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user):
    subject = "Your Verification Code"
    message = f"Hello {user.username},\n\nYour verification code is: {user.code.number}.\n\nPlease enter this code to complete your login process."
    recipient_list = [user.email]  # The user's email address

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # From email
        recipient_list,
        fail_silently=False,  # Raise an error if sending fails
    )
