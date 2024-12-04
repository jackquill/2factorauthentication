# from users.models import CustomUser
# from .models import Code
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# # automatically generate a Code object whenever a new CustomUser
# @receiver(post_save, sender= CustomUser)
# def post_save_generate_code(sender, instance, created, *args, **kwargs):
#     if created:
#         Code.objects.create(user=instance)


from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from .models import Code
import secrets
import string

def generate_new_code():
    # Generate a new 5-character random code (digits only)
    return ''.join(secrets.choice(string.digits) for i in range(5))

@receiver(post_save, sender=CustomUser)
def post_save_generate_code(sender, instance, created, **kwargs):
    print("post save entered")
    # If the CustomUser is newly created
    if created:
        # Generate and create a new Code for the user
        Code.objects.create(user=instance)

