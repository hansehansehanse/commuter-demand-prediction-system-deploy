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


#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

from django.db import models
import uuid

class ActionLog(models.Model):
    user_code = models.ForeignKey('CustomUser', on_delete=models.CASCADE, to_field='user_code')
    action = models.CharField(max_length=255)  # Short action type (example: "Create User")
    details = models.TextField(blank=True)     # Longer optional details
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.user_code} on {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

# from django.db import models
# from django.contrib.auth import get_user_model
# import uuid

# User = get_user_model()

# class Dataset(models.Model):
#     dataset_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     date = models.DateField()
#     route = models.CharField(max_length=100)
#     time = models.TimeField()
#     num_commuters = models.IntegerField()
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     user_code = models.UUIDField()                                                                  #!!!
#     filename = models.CharField(max_length=255, blank=True, null=True)
#     date_uploaded = models.DateTimeField(auto_now_add=True)

#     day_of_week = models.CharField(max_length=20, blank=True)
#     day = models.CharField(max_length=20, null=True, blank=True)
#     month = models.CharField(max_length=20, blank=True)
#     is_holiday = models.BooleanField(default=False)
#     is_friday = models.BooleanField(default=False)
#     is_saturday = models.BooleanField(default=False)

#     is_day_before_holiday = models.BooleanField(default=False)                                      #!!!
#     is_long_weekend = models.BooleanField(default=False)                                            #!!!
#     is_day_before_long_weekend = models.BooleanField(default=False)                                 #!!!      

#     is_local_holiday = models.BooleanField(default=False)
#     is_university_event = models.BooleanField(default=False)
#     is_local_event = models.BooleanField(default=False)
#     is_others = models.BooleanField(default=False)
#     is_flagged = models.BooleanField(default=False)


#     is_within_ay = models.BooleanField(default=False)

#     is_start_of_sem=models.BooleanField(default=False)

#     is_day_before_end_of_sem=models.BooleanField(default=False)
#     is_week_before_end_of_sem=models.BooleanField(default=False)
#     is_end_of_sem=models.BooleanField(default=False)    
#     is_day_after_end_of_sem=models.BooleanField(default=False)
#     is_2days_after_end_of_sem=models.BooleanField(default=False)
#     is_week_after_end_of_sem=models.BooleanField(default=False)


#-------------------------------------------------------------------------
#-------------------------------------------------------------------------


#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class TemporalEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('local_holiday', 'Local Holiday'),
        ('university_event', 'University Event'),
        ('local_event', 'Local Event'),
        ('others', 'Others'),
    ]

    event_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    event_name = models.CharField(max_length=255)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    date = models.DateField(null=True, blank=True)

    sort_order = models.PositiveIntegerField(default=0)

    created_by = models.UUIDField(null=True, blank=True)  # Allow null initially
    updated_by = models.UUIDField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#-------------------------------------------------------------------------

class HolidayEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('holiday', 'Holiday'),
    ]

    # Primary fields
    event_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    event_name = models.CharField(max_length=255)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    date = models.DateField(null=True, blank=True)  # Stores only the month and day

    # Tracking fields
    updated_by = models.UUIDField(null=True, blank=True)  # UUID of the user who last updated it
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated timestamp when the object is updated

    def save(self, *args, **kwargs):
        # Store the date without the year (set it to January 1st if no year is given)
        if self.date:
            self.date = self.date.replace(year=1900)  # Year doesn't matter, just replace it with a dummy value
        super().save(*args, **kwargs)

    def __str__(self):
        return self.event_name


#-------------------------------------------------------------------------

class HistoricalDataset(models.Model):
    dataset_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date = models.DateField()
    route = models.CharField(max_length=100)
    time = models.TimeField()
    num_commuters = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user_code = models.UUIDField()                                                                  #!!!
    filename = models.CharField(max_length=255, blank=True, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    day_of_week = models.CharField(max_length=20, blank=True)
    # day = models.CharField(max_length=20, null=True, blank=True)
    month = models.CharField(max_length=20, blank=True)
    is_holiday = models.BooleanField(default=False)
    is_friday = models.BooleanField(default=False)
    is_saturday = models.BooleanField(default=False)

    is_day_before_holiday = models.BooleanField(default=False)                                      #!!!
    is_long_weekend = models.BooleanField(default=False)                                            #!!!
    is_day_before_long_weekend = models.BooleanField(default=False)                                 #!!!      

    is_local_holiday = models.BooleanField(default=False)
    is_university_event = models.BooleanField(default=False)
    is_local_event = models.BooleanField(default=False)
    is_others = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)


    is_within_ay = models.BooleanField(default=False)

    is_start_of_sem=models.BooleanField(default=False)

    is_day_before_end_of_sem=models.BooleanField(default=False)
    is_week_before_end_of_sem=models.BooleanField(default=False)
    is_end_of_sem=models.BooleanField(default=False)    
    is_day_after_end_of_sem=models.BooleanField(default=False)
    is_2days_after_end_of_sem=models.BooleanField(default=False)
    is_week_after_end_of_sem=models.BooleanField(default=False)




from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class HistoricalTemporalEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('local_holiday', 'Local Holiday'),
        ('university_event', 'University Event'),
        ('local_event', 'Local Event'),
        ('others', 'Others'),
    ]

    event_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    event_name = models.CharField(max_length=255)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    date = models.DateField(null=True, blank=True)

    sort_order = models.PositiveIntegerField(default=0)

    created_by = models.UUIDField(null=True, blank=True)  # Allow null initially
    updated_by = models.UUIDField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



from django.db import models
from django.utils import timezone
import uuid

class ModelTrainingHistory(models.Model):
    training_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    trained_by = models.UUIDField(null=True, blank=True)
    trained_at = models.DateTimeField(auto_now_add=True)

    model_type = models.CharField(max_length=100, default='Random Forest')
    model_name = models.CharField(max_length=255, editable=False)

    rmse = models.FloatField()
    mae = models.FloatField()

    oldest_date = models.DateField()
    latest_date = models.DateField()

    notes = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.model_name} (Trained by {self.trained_by})"
