# signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from .models import CustomUser

@receiver(user_logged_in)
def update_last_logged_in(sender, request, user, **kwargs):
    if isinstance(user, CustomUser):
        user.last_logged_in = timezone.now()  # Set the current time
        user.save()  # Save the user object with the updated timestamp
