from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


# Simple phone number validator (You can modify the regex to fit your use case)
def validate_phone_number(value):
    phone_regex = r'^\+?\d{10,15}$'  # Example: international format (e.g., +1234567890)
    if not re.match(phone_regex, value):
        raise ValidationError(f"{value} is not a valid phone number.")

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator  # Import for phone validation

# Phone number validator (you can customize this regex)
validate_phone_number = RegexValidator(
    regex=r'^\+?\d{9,15}$',
    message="Enter a valid phone number (up to 15 digits, optional '+' sign)."
)

class CustomUser(AbstractUser):
    user_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, validators=[validate_phone_number], null=True, blank=True)
    email = models.EmailField(unique=True)
    verified = models.BooleanField(default=False)
    access_level = models.CharField(
        max_length=20,
        choices=[('Admin', 'Admin'), ('Bus Manager', 'Bus Manager')],
        default='Bus Manager'
    )
    # last_logged_in = models.DateTimeField(null=True, blank=True) 

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return f"{self.username} ({self.user_code})"
