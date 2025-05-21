
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import make_password
from .models import CustomUser
import json
import uuid
import logging
from .models import ActionLog  
from django.contrib import messages



#-------------------------------------------------------------------------
from datetime import date
from .models import HolidayEvent, TemporalEvent, HistoricalTemporalEvent


def build_holiday_set():
    holidays = set()
    holiday_events = HolidayEvent.objects.all()
    # print(f"[build_holiday_set] Found {holiday_events.count()} HolidayEvent(s).")

    for h in holiday_events:
        # print(f"  → Processing holiday: {h.event_name} on {h.date}")
        for year in range(2000, 2101):  # Reasonable test range
            full_date = date(year, h.date.month, h.date.day)
            holidays.add(full_date)
    
    # print(f"[build_holiday_set] Total generated holiday dates: {len(holidays)}")
    return holidays

def build_local_holiday_set():
    local_holidays = set()

    temporal_qs = TemporalEvent.objects.filter(event_type='local_holiday').exclude(date=None)
    # print(f"[build_local_holiday_set] Found {temporal_qs.count()} TemporalEvent(s) with 'local_holiday'.")

    for t in temporal_qs:
        # print(f"  → TemporalEvent: {t.event_name} on {t.date}")
        local_holidays.add(t.date)

    historical_qs = HistoricalTemporalEvent.objects.filter(event_type='local_holiday').exclude(date=None)
    # print(f"[build_local_holiday_set] Found {historical_qs.count()} HistoricalTemporalEvent(s) with 'local_holiday'.")

    for h in historical_qs:
        # print(f"  → HistoricalTemporalEvent: {h.event_name} on {h.date}")
        local_holidays.add(h.date)

    # print(f"[build_local_holiday_set] Total unique local holiday dates: {len(local_holidays)}")
    return local_holidays

def is_any_holiday(d, holiday_set, local_holiday_set):
    return any(d == holiday for holiday in holiday_set) or \
           any(d == local_holiday for local_holiday in local_holiday_set)

from datetime import timedelta

def is_day_before_any_holiday(d, holiday_set, local_holiday_set):
    return (
        (d + timedelta(days=1)) in holiday_set or
        (d + timedelta(days=1)) in local_holiday_set
    )
from datetime import timedelta

# !!! still needs some tweaking
def is_any_long_weekend(d, holiday_set, local_holiday_set):
    def is_long_weekend_for_set(date, holidays):
        weekday = date.weekday()
        
        # Define nearby days
        prev_day = date - timedelta(days=1)
        next_day = date + timedelta(days=1)
        two_days_after = date + timedelta(days=2)
        two_days_before = date - timedelta(days=2)
        
        # If the date itself is a holiday (not required but can be useful context)
        is_holiday = date in holidays

        # Classic Friday-Monday long weekends
        friday_case = weekday == 4 and (next_day in holidays or two_days_after in holidays)  # Friday + Sat/Sun
        monday_case = weekday == 0 and (two_days_before in holidays or prev_day in holidays)  # Mon + Sat/Sun
        
        # Thursday holiday leading into Friday off (bridge)
        thursday_case = weekday == 3 and next_day in holidays

        # Tuesday holiday after a Monday off
        tuesday_case = weekday == 1 and prev_day in holidays

        return friday_case or monday_case or thursday_case or tuesday_case

    return (
        is_long_weekend_for_set(d, holiday_set) or
        is_long_weekend_for_set(d, local_holiday_set)
    )


def is_day_before_any_long_weekend(d, holiday_set, local_holiday_set):
    next_day = d + timedelta(days=1)
    return is_any_long_weekend(next_day, holiday_set, local_holiday_set)



#-------------------------------------------------------------------------

#-------------------------------------------------------------------------


def check_local_holiday_flag(target_date):
    return (
        TemporalEvent.objects.filter(date=target_date, event_type='local_holiday').exists() or
        HistoricalTemporalEvent.objects.filter(date=target_date, event_type='local_holiday').exists()
    )

def check_university_event_flag(target_date):
    return (
        TemporalEvent.objects.filter(date=target_date, event_type='university_event').exists() or
        HistoricalTemporalEvent.objects.filter(date=target_date, event_type='university_event').exists()
    )

def check_local_event_flag(target_date):
    return (
        TemporalEvent.objects.filter(date=target_date, event_type='local_event').exists() or
        HistoricalTemporalEvent.objects.filter(date=target_date, event_type='local_event').exists()
    )

def check_others_event_flag(target_date):
    return (
        TemporalEvent.objects.filter(date=target_date, event_type='others').exists() or
        HistoricalTemporalEvent.objects.filter(date=target_date, event_type='others').exists()
    )


def get_university_semester_flags(target_date):
    flags = {
        'is_within_ay': False,
        'is_start_of_sem': False,
        'is_day_before_end_of_sem': False,
        'is_week_before_end_of_sem': False,
        'is_end_of_sem': False,
        'is_day_after_end_of_sem': False,
        'is_2days_after_end_of_sem': False,
        'is_week_after_end_of_sem': False
    }

    # Fetch events from both models
    temporal_events = TemporalEvent.objects.filter(event_type='university_event')
    historical_events = HistoricalTemporalEvent.objects.filter(event_type='university_event')

    # Combine and filter start/end events
    combined_events = list(temporal_events) + list(historical_events)
    sem_starts = sorted(
        [e for e in combined_events if 'Start of' in e.event_name],
        key=lambda e: e.date
    )
    sem_ends = sorted(
        [e for e in combined_events if 'End of' in e.event_name],
        key=lambda e: e.date
    )

    for start_event, end_event in zip(sem_starts, sem_ends):
        start_date = start_event.date
        end_date = end_event.date

        # Logging semester range
        print(f"[Semester] Start of: {start_date} | End of: {end_date}")

        if start_date <= target_date <= end_date:
            flags['is_within_ay'] = True
        if target_date == start_date:
            flags['is_start_of_sem'] = True
        if target_date == end_date - timedelta(days=1):
            flags['is_day_before_end_of_sem'] = True
        if end_date - timedelta(days=7) <= target_date < end_date:
            flags['is_week_before_end_of_sem'] = True
        if target_date == end_date:
            flags['is_end_of_sem'] = True
        if target_date == end_date + timedelta(days=1):
            flags['is_day_after_end_of_sem'] = True
        if target_date == end_date + timedelta(days=2):
            flags['is_2days_after_end_of_sem'] = True
        if end_date < target_date <= end_date + timedelta(days=7):
            flags['is_week_after_end_of_sem'] = True

    return flags



#-------------------------------------------------------------------------
#-------------------------------------------------------------------------


#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_backends
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            print("👤 Match found in DB:", user)

            if check_password(password, user.password):
                print("✅ Password matches!")
                print("🔎 Access level from DB:", user.access_level)              


                # Explicitly specify the backend to avoid ValueError
                backend = get_backends()[0]
                login(request, user, backend=backend.__class__.__module__ + "." + backend.__class__.__name__)

                if user.access_level == 'Admin':
                    log_action(request, 'Login', f"User {user.first_name} {user.last_name} logged in.")
                    return redirect(reverse('dashboard'))
                
                elif user.access_level == 'Bus Manager':
                    log_action(request, 'Login', f"User {user.first_name} {user.last_name} logged in.")
                    return redirect('cdps_admin_dashboard')                             # update!!!
                
                else:
                    print("❓ Unknown access level")
                    return render(request, 'login.html', {'error': 'Access level not recognized'})
            else:
                print("❌ Password does not match.")
                return render(request, 'login.html', {'error': 'Invalid password'})
        except User.DoesNotExist:
            print("❌ No user found with that email.")
            return render(request, 'login.html', {'error': 'Invalid email'})

    return render(request, 'login.html')

#--


#--


#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
# from django.shortcuts import render
# from .models import CustomUser

def user_list(request):
    print("✅ user_list being called")
    users = CustomUser.objects.all()
    print(f"🧾 Users in DB: {users}")
    return render(request, 'admin/accountManagement.html', {'users': users})

#-------------------------------------------------------------------------
from django.contrib.auth import get_user_model
import json
import uuid
import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)

# Get the user model dynamically
User = get_user_model()

def add_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse the JSON body
            print("📩 Received data:", data)  # Log the received data

            email = data.get('email', '').strip().lower()  # Normalize the email
            print("Normalized email:", email)

            # Check if email already exists using the dynamic user model
            if User.objects.filter(email=email).exists():
                print("Email already in use!")
                return JsonResponse({'status': 'error', 'message': 'Email is already in use.'}, status=400)

            # If no error, create the user
            user = User.objects.create_user(
                username=str(uuid.uuid4()),
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', ''),
                email=email,  # Use the normalized email
                phone_number=data.get('phone_number', ''),
                access_level=data.get('access_level', 'Bus Manager'),
                verified=data.get('verified', False),
                password=data.get('password', 'temporary123'),
            )

            log_action(request, 'Add User', f"User {user.first_name} {user.last_name} account added.")



            return JsonResponse({'status': 'success'}, status=201)

        except Exception as e:
            print("❌ Exception:", e)
            logger.error(f"Error adding user: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Error occurred while adding user.'}, status=500)


#-------------------------------------------------------------------------

def edit_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_code = data.get("user_code")
            user = CustomUser.objects.get(user_code=user_code)

            log_action(request, 'Edit User', f"User {user.first_name} {user.last_name} information adjusted.")
            # Update fields
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.email = data["email"]
            user.phone_number = data["phone_number"]
            user.access_level = data["access_level"]
            user.verified = data["verified"]

            if data["password"]:  # Only update if password is provided
                user.password = make_password(data["password"])

           
            user.save()
            return JsonResponse({"message": "User updated successfully."})
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)

#-------------------------------------------------------------------------
# from django.views.decorators.http import require_POST

@require_POST
def delete_user(request):
    try:
        data = json.loads(request.body)
        user_code = data.get("user_code")
        user = CustomUser.objects.get(user_code=user_code)
        log_action(request, 'Delete User', f"User {user.first_name} {user.last_name} account deleted.")
        user.delete()
        return JsonResponse({"message": "User deleted successfully."})
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

#-------------------------------------------------------------------------

from .models import ActionLog

User = get_user_model()

def log_action(request, action_type, details=""):
    # Access the currently logged-in user
    user = request.user  # This is the correct way to access the logged-in user
    if user.is_authenticated:  # Now check on user, not request
        action_log = ActionLog(
            user_code=user,
            action=action_type,
            details=details
        )
        action_log.save()
    else:
        print("No user is logged in!")

from django.shortcuts import render
from .models import ActionLog

def action_log_list(request):
    print("✅ action_log_list being called")
    
    # Fetch all action logs from the database
    actions = ActionLog.objects.all().order_by('-timestamp')  # Optionally order by timestamp (most recent first)
    
    print(f"🧾 Action Logs in DB: {actions}")
    
    # Render the action logs in the template
    return render(request, 'admin/actionLog.html', {'actions': actions})



#-------------------------------------------------------------------------
# XXX
# from django.contrib.auth import get_user_model
# from .models import Dataset, HolidayEvent, TemporalEvent
# import pandas as pd
# from datetime import datetime
# from django.shortcuts import render, redirect

# User = get_user_model()

# def dataset_upload_list(request):
#     if request.method == 'POST':
#         dataset_file = request.FILES.get('dataset_file')
#         if dataset_file:
#             file_extension = dataset_file.name.split('.')[-1]
#             if file_extension == 'xlsx':
#                 df = pd.read_excel(dataset_file)
                
#             elif file_extension == 'csv':
#                 df = pd.read_csv(dataset_file)
                

#             user = request.user
#             # print(f"User Code: {user.user_code}")  # Debug

#             holidays = build_holiday_set()  # Build once

#             for _, row in df.iterrows():
#                 try:
#                     date_val = pd.to_datetime(row['Date']).date()
#                 except Exception as e:
#                     print(f"Error parsing date: {e}")
#                     continue

#                 route = row['Route']
#                 try:
#                     time_val = datetime.strptime(row['Time'], "%I:%M %p").strftime("%H:%M")
#                 except ValueError as e:
#                     print(f"Error parsing time: {e}")
#                     continue


#                 num_commuters = row['Commuters']

#                 day_of_week = date_val.strftime("%A")
#                 month = date_val.strftime("%B")
#                 weekday = date_val.weekday()
#                 is_friday = weekday == 4
#                 is_saturday = weekday == 5

#                 is_holiday = date_val in holidays
#                 is_before_holiday = is_day_before_holiday(date_val, holidays)
#                 is_lweekend = is_long_weekend(date_val, holidays)
#                 is_before_lweekend = is_day_before_long_weekend(date_val, holidays)

#                 is_local_holiday = check_local_holiday_flag(date_val)
#                 is_university_event = check_university_event_flag(date_val)
#                 is_local_event = check_local_event_flag(date_val)
#                 is_others = check_others_event_flag(date_val)

#                 semester_flags = get_university_semester_flags(date_val)

#                 is_within_ay = semester_flags['is_within_ay']
#                 is_start_of_sem = semester_flags['is_start_of_sem']
#                 is_day_before_end_of_sem = semester_flags['is_day_before_end_of_sem']
#                 is_week_before_end_of_sem = semester_flags['is_week_before_end_of_sem']
#                 is_end_of_sem = semester_flags['is_end_of_sem']
#                 is_day_after_end_of_sem = semester_flags['is_day_after_end_of_sem']
#                 is_2days_after_end_of_sem = semester_flags['is_2days_after_end_of_sem']
#                 is_week_after_end_of_sem = semester_flags['is_week_after_end_of_sem']


#                 # print(
#                 #     f"Date: {date_val} | "
#                 #     f"is_within_ay: {is_within_ay}, "
#                 #     f"is_start_of_sem: {is_start_of_sem}, "
#                 #     f"is_day_before_end_of_sem: {is_day_before_end_of_sem}, "
#                 #     f"is_week_before_end_of_sem: {is_week_before_end_of_sem}, "
#                 #     # f"is_end_of_sem: {is_end_of_sem}, "
#                 #     # f"is_day_after_end_of_sem: {is_day_after_end_of_sem}, "
#                 #     # f"is_2days_after_end_of_sem: {is_2days_after_end_of_sem}, "
#                 #     # f"is_week_after_end_of_sem: {is_week_after_end_of_sem}"
#                 # )

#                 # print(
#                 #     f"Date: {date_val} | "
#                 #     # f"is_within_ay: {is_within_ay}, "
#                 #     # f"is_start_of_sem: {is_start_of_sem}, "
#                 #     # f"is_day_before_end_of_sem: {is_day_before_end_of_sem}, "
#                 #     # f"is_week_before_end_of_sem: {is_week_before_end_of_sem}, "
#                 #     f"is_end_of_sem: {is_end_of_sem}, "
#                 #     f"is_day_after_end_of_sem: {is_day_after_end_of_sem}, "
#                 #     f"is_2days_after_end_of_sem: {is_2days_after_end_of_sem}, "
#                 #     f"is_week_after_end_of_sem: {is_week_after_end_of_sem}"
#                 # )


#                 Dataset.objects.create(
#                     date=date_val,
#                     route=route,
#                     time=time_val,
#                     num_commuters=num_commuters,
#                     user_code=user.user_code,
#                     filename=dataset_file.name,

#                     day=day_of_week,
#                     month=month,
#                     is_friday=is_friday,
#                     is_saturday=is_saturday,
#                     is_holiday=is_holiday,
#                     is_day_before_holiday=is_before_holiday,
#                     is_long_weekend=is_lweekend,
#                     is_day_before_long_weekend=is_before_lweekend,

#                     # Temporal event flags
#                     is_local_holiday=is_local_holiday,
#                     is_university_event=is_university_event,
#                     is_local_event=is_local_event,
#                     is_others=is_others,

#                     # Semester-related flags
#                     is_within_ay=is_within_ay,
#                     is_start_of_sem=is_start_of_sem,
#                     is_day_before_end_of_sem=is_day_before_end_of_sem,
#                     is_week_before_end_of_sem=is_week_before_end_of_sem,
#                     is_end_of_sem=is_end_of_sem,
#                     is_day_after_end_of_sem=is_day_after_end_of_sem,
#                     is_2days_after_end_of_sem=is_2days_after_end_of_sem,
#                     is_week_after_end_of_sem=is_week_after_end_of_sem
#                 )

#                 log_action(request, 'Dataset Upload', f"User {user.first_name} {user.last_name} upload dataset.")


#             return redirect('dataset_upload_list')

#     datasets = Dataset.objects.all()

#     user_map = {
#         u.user_code: u for u in User.objects.filter(user_code__in=[d.user_code for d in datasets])
#     }

#     for d in datasets:
#         d.uploader = user_map.get(d.user_code)

#     return render(request, 'admin/datasetUpload.html', {'datasets': datasets})

#-------------------------------------------------------------------------

# views.py
from django.shortcuts import render
from CommuterDemandPredictionSystem.models import HolidayEvent, TemporalEvent
from django.contrib.auth import get_user_model

User = get_user_model()

def event_list(request):
    # Fetch all records
    holidays = HolidayEvent.objects.all().order_by('date')
    events = TemporalEvent.objects.all().order_by('date')

    events = TemporalEvent.objects.all().order_by('event_type', 'sort_order')


    user_map = {user.user_code: user for user in User.objects.all()}
    for event in events:
        event.created_by_user = user_map.get(event.created_by)
        event.updated_by_user = user_map.get(event.updated_by)

    context = {
        'holidays': holidays,
        'events': events,
    }
    return render(request, 'admin/datasetTemporal.html', context)

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
#CRUD FOR RECENT EVENTS!
from django.shortcuts import render
from django.http import JsonResponse
from .models import TemporalEvent
from django.contrib.auth import get_user_model
import json
import logging
import uuid

# Logger
logger = logging.getLogger(__name__)

User = get_user_model()

def add_event(request):
    # print("------------------------------------------------------------------------------Add event view triggered!")
    if request.method == 'POST':
        try:
            # Get data from the request body (parsed from JSON)
            data = json.loads(request.body)  # Parse the JSON body
            print("📩 Received event data:", data)  # Log the received data

            # Extract form data
            event_name = data.get('event_name', '').strip()
            event_type = data.get('event_type', '')
            event_date = data.get('date', None)

            # Normalize the event type
            if event_type not in dict(TemporalEvent.EVENT_TYPE_CHOICES):
                return JsonResponse({'status': 'error', 'message': 'Invalid event type.'}, status=400)

            # Check if an event with the same name already exists (optional validation)
            if TemporalEvent.objects.filter(event_name=event_name, date=event_date).exists():
                return JsonResponse({'status': 'error', 'message': 'Event with the same name and date already exists.'}, status=400)

            # Get the user who is creating the event and assign their UUID (not the numeric id)
            created_by_user = request.user.user_code  # Ensure you're using the user_code UUID here

            # Create the new event
            event = TemporalEvent.objects.create(
                event_name=event_name,
                event_type=event_type,
                date=event_date,
                created_by=created_by_user,  # Assign the current user's UUID
                updated_by=created_by_user,  # Initial update by the creator
            )

            # Log the action (for audit purposes)
            log_action(request, 'Add Event', f"Event {event.event_name} created by {request.user.first_name} {request.user.last_name}.")

            return JsonResponse({'status': 'success'}, status=201)

        except Exception as e:
            logger.error(f"Error adding event: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Error occurred while adding event.'}, status=500)

#-------------------------------------------------------------------------
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from .models import TemporalEvent  # Import the model

User = get_user_model()

def edit_event(request):
    print("Edit event view triggered!") 
    if request.method == "POST":
        try:
            # Parse incoming data
            data = json.loads(request.body)
            event_code = data.get("event_code")  # Get the event code to identify the event
            print(f"EDIT EVENT: Received event code to edit: {event_code}")
            event = get_object_or_404(TemporalEvent, event_code=event_code)  # Find event by event_code

            # Capture the logged-in user's UUID
            updated_by = request.user.user_code  # Assuming your user model has `user_code` field

            # Log the action (You can also use some action logging if required)
            log_action(request, 'Edit Event', f"Event {event.event_name} updated.")

            # Before updating, print the data that was received
            print(f"Received data to update event: {data}")

            # Update the event fields with data from the request
            event.event_name = data["event_name"]
            event.event_type = data["event_type"]
            event.date = data["date"]  # Assume the 'date' comes as a valid date string
            event.updated_by = updated_by  # Update the `updated_by` field with the logged-in user's UUID
            
            # Save the updated event object
            event.save()
            log_action(request, 'Edit Event', f"Event {event.event_name} edited by {request.user.first_name} {request.user.last_name}.")
            # Print the updated event to check if the changes were applied
            print(f"Updated event: {event.event_name}, {event.event_type}, {event.date}, updated by: {event.updated_by}")

            # Return a success response
            return JsonResponse({'status': 'success', 'message': 'Event updated successfully'})

        except Exception as e:
            # Print error to the console for debugging
            print(f"Error: {e}")
            # Return error message if something goes wrong
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from .models import TemporalEvent

def delete_event(request):
    print("Delete event view triggered!")

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            event_code = data.get("event_code")
            

            print(f"DELETE EVENT: Received event code to delete: {event_code}")
            if not event_code:
                return JsonResponse({'status': 'error', 'message': 'Event code is required.'}, status=400)

            event = get_object_or_404(TemporalEvent, event_code=event_code)

            log_action(request, 'Delete Event', f"Event {event.event_name} deleted by {request.user.first_name} {request.user.last_name}.")

            event.delete()

            print(f"✅ Deleted event with code: {event_code}")
            return JsonResponse({'status': 'success', 'message': 'Event deleted successfully'})

        except Exception as e:
            print(f"❌ Error deleting event: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)



#-------------------------------------------------------------------------
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from .models import HolidayEvent  # Import your HolidayEvent model

User = get_user_model()

def edit_holiday_event(request):
    print("Edit holiday event view triggered!") 
    if request.method == "POST":
        try:
            # Parse incoming data
            data = json.loads(request.body)
            event_code = data.get("event_code")  # Get the event code to identify the event
            event = get_object_or_404(HolidayEvent, event_code=event_code)  # Find event by event_code

            # Capture the logged-in user's UUID
            updated_by = request.user.user_code  # Assuming your user model has `user_code` field

            # Log the action (You can also use some action logging if required)
            log_action(request, 'Edit Holiday Event', f"Holiday Event {event.event_name} updated.")

            # Before updating, print the data that was received
            print(f"Received data to update holiday event: {data}")


            # Update the holiday event fields with data from the request
            event.event_name = data["event_name"]
            # event.event_type = data["event_type"]
            event.date = data["date"]  # Assume the 'date' comes as a valid date string
            event.updated_by = updated_by  # Update the `updated_by` field with the logged-in user's UUID
            
            
            # Save the updated event object
            event.save()
            log_action(request, 'Edit Holiday Event', f"Holiday Event {event.event_name} edited by {request.user.first_name} {request.user.last_name}.")
            # Print the updated event to check if the changes were applied
            print(f"Updated holiday event: {event.event_name}, {event.date}, updated by: {event.updated_by}")

            # Return a success response
            return JsonResponse({'status': 'success', 'message': 'Holiday Event updated successfully'})

        except Exception as e:
            # Print error to the console for debugging
            print(f"Error: {e}")
            # Return error message if something goes wrong
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


#-------------------------------------------------------------------------

# XXX
# from django.shortcuts import render
# from .cdps import train_and_predict_random_forest

# def predict_commuters(request):
#     # Get the predictions for the next 2 weeks
#     predictions = train_and_predict_random_forest()

#     # Render the predictions in the table format
#     return render(request, 'admin/datasetPrediction.html', {'predictions': predictions})

#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
#datasetGraph.html
def dataset_graph(request):

    if request.method == "POST":
        graph_type = request.POST.get("graph_type")  
        route = request.POST.get("route")
        time_str = request.POST.get("time")
        selected_date = request.POST.get("date")  

        # print(f"Graph Type: {graph_type}")
        # print(f"1 Route: {route}, Time: {time_str}, Selected Date: {selected_date}")

        if not route or not time_str:
            return JsonResponse({'error': 'Missing route or time'})

        # Handle different graph types
        if graph_type == "last7":
            print("FROM: last7")
            return get_last_7_records_chart_data(route, time_str)

        elif graph_type == "average_from_date":
            print("FROM: average_from_date")
            # print(f"Route: {route}, Time: {time_str}, Selected Date: {selected_date}")
            return get_average_commuters_from_date(route, time_str, selected_date)
        
        elif graph_type == "rf_prediction":
            print("FROM: rf_prediction")
            return rf_predict_commuters(route, time_str, selected_date)

        elif graph_type == 'two_week_predictions':
            print("FROM: two_week_predictions")
            return rf_predict_commuters_2weeks(route, time_str, selected_date)

        return JsonResponse({'error': 'Unknown graph_type'})

    return render(request, 'admin/datasetGraph.html', {
        'bus_schedule': {
            "A to B": ["5:00AM", "1:00PM", "6:00PM"],
            "A to C": ["5:30AM"]
        }
    })


from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import HistoricalDataset
import json

def get_last_7_records_chart_data(route, time_str):
    try:
        time_obj = datetime.strptime(time_str, "%I:%M%p").time()
    except ValueError:
        return JsonResponse({'error': 'Invalid time format'})

    # Get the latest 7 historical entries for that route & time
    results = HistoricalDataset.objects.filter(route=route, time=time_obj).order_by('-date')[:7]
    results = sorted(results, key=lambda x: x.date)  # Ascending order for the chart

    dates = [r.date.strftime('%Y-%m-%d') for r in results]
    num_commuters = [r.num_commuters for r in results]

    chart_data = {
        'dates': dates,
        'num_commuters': num_commuters,
    }
    # print("get_last_7_records_chart_data")
    return JsonResponse({'chart_data': json.dumps(chart_data)})


from .models import HistoricalDataset
from django.db.models import Avg
from datetime import datetime
from django.http import JsonResponse

def get_average_commuters_from_date(route, time_str, selected_date):
    
    try:
        # Parse inputs
        date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
        time_obj = datetime.strptime(time_str, "%I:%M%p").time()  # 12hr to 24hr

        # Try to find the latest available date on or before the selected date
        latest_available = HistoricalDataset.objects.filter(
            route=route,
            time=time_obj,
            date__lte=date_obj
        ).order_by('-date').first()

        if not latest_available:
            print("❌ No matching records found at all.")
            return JsonResponse({'average': 0})

        fallback_date = latest_available.date
        print(f"✅ Using fallback date range: earliest up to {fallback_date}")

        # Get all matching records up to the fallback date
        matching_records = HistoricalDataset.objects.filter(
            route=route,
            time=time_obj,
            date__lte=fallback_date
        )

        # print(f"🔍 Matching records for route='{route}', time='{time_obj}', date ≤ {fallback_date}:")
        # for record in matching_records:
        #     print(f"  🚌 ID: {record.id}, Date: {record.date}, Count: {record.num_commuters}")


        total = 0
        count = 0

        # print("\n📋 Starting manual average computation:")
        for record in matching_records:
            prev_total = total
            prev_count = count

            total += record.num_commuters
            count += 1

            # print(
            #     f"  ➕ Record ID {record.id} | Date: {record.date} | "
            #     f"Commuters: {record.num_commuters} | "
            #     f"Prev Total: {prev_total} ➝ New Total: {total} | "
            #     f"Prev Count: {prev_count} ➝ New Count: {count}"
            # )

        if count > 0:
            average = total / count
            print(f"\n✅ Final Total: {total}")
            print(f"📌 Final Count: {count}")
            print(f"📊 Computed Average: {round(average, 2)}")
        else:
            average = 0
            print("⚠️ No records to compute average from.")

        return JsonResponse({'average': round(average, 2)})


    except Exception as e:
        print("❌ Error in get_average_commuters_from_date:", e)
        return JsonResponse({'error': 'Failed to compute average'}, status=500)

####
# from django.conf import settings
# import os
# import joblib
# from django.http import JsonResponse
# from datetime import datetime

# # Load the pre-trained model using the method you suggested
# def load_pretrained_model():
#     try:
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         model_path = os.path.join(current_dir, 'model', 'random_forest_model.pkl')

#         print(f"📍 Corrected Model Path: {model_path}")
#         print(f"📁 File Exists: {os.path.exists(model_path)}")

#         if not os.path.exists(model_path):
#             return None  # Model not found

#         model = joblib.load(model_path)
#         print("✅ Model loaded!")
#         print(f"📦 Model Type: {type(model)}")
#         return model

#     except Exception as e:
#         print("❌ Error loading model")
#         print(f"❌ Exception: {str(e)}")
#         return None

# def load_feature_list():
#     try:
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         features_path = os.path.join(current_dir, 'model', 'features_used.pkl')

#         print(f"📍 Feature List Path: {features_path}")
#         print(f"📁 File Exists: {os.path.exists(features_path)}")

#         if not os.path.exists(features_path):
#             return None  # Feature list not found

#         features = joblib.load(features_path)
#         print("✅ Features loaded!")
#         return features

#     except Exception as e:
#         print("❌ Error loading features list")
#         print(f"❌ Exception: {str(e)}")
#         return None

# def load_route_encoder():
#     try:
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         encoder_path = os.path.join(current_dir, 'model', 'route_encoder.pkl')

#         print(f"📍 Route Encoder Path: {encoder_path}")
#         print(f"📁 File Exists: {os.path.exists(encoder_path)}")

#         if not os.path.exists(encoder_path):
#             return None

#         route_encoder = joblib.load(encoder_path)
#         print("✅ Route encoder loaded!")
#         return route_encoder

#     except Exception as e:
#         print("❌ Error loading route encoder")
#         print(f"❌ Exception: {str(e)}")
#         return None

import os
import joblib
from django.conf import settings

def load_pretrained_model():
    try:
        model_path = settings.MODEL_PATH
        print(f"📍 Model Path from settings: {model_path}")
        print(f"📁 File Exists: {os.path.exists(model_path)}")

        if not os.path.exists(model_path):
            return None

        model = joblib.load(model_path)
        print("✅ Model loaded!")
        print(f"📦 Model Type: {type(model)}")
        return model

    except Exception as e:
        print("❌ Error loading model")
        print(f"❌ Exception: {str(e)}")
        return None

def load_feature_list():
    try:
        features_path = settings.FEATURES_PATH
        print(f"📍 Feature List Path from settings: {features_path}")
        print(f"📁 File Exists: {os.path.exists(features_path)}")

        if not os.path.exists(features_path):
            return None

        features = joblib.load(features_path)
        print("✅ Features loaded!")
        return features

    except Exception as e:
        print("❌ Error loading features list")
        print(f"❌ Exception: {str(e)}")
        return None

def load_route_encoder():
    try:
        encoder_path = settings.ROUTE_ENCODER_PATH
        print(f"📍 Route Encoder Path from settings: {encoder_path}")
        print(f"📁 File Exists: {os.path.exists(encoder_path)}")

        if not os.path.exists(encoder_path):
            return None

        route_encoder = joblib.load(encoder_path)
        print("✅ Route encoder loaded!")
        return route_encoder

    except Exception as e:
        print("❌ Error loading route encoder")
        print(f"❌ Exception: {str(e)}")
        return None


import pandas as pd
import joblib
from datetime import datetime
from django.http import JsonResponse

def rf_predict_commuters(route, time_str, selected_date):
    model = load_pretrained_model()
    features_to_use = load_feature_list()
    
    if model is None or features_to_use is None:
        return JsonResponse({'error': 'Model or feature list loading failed'}, status=500)

    # Parse inputs
    try:
        date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
        time_obj = datetime.strptime(time_str, "%I:%M%p").time()  # 12hr to 24hr
    except ValueError:
        return JsonResponse({'error': 'Invalid date or time format'}, status=400)

    hour = time_obj.hour
    weekday = date_obj.weekday()

    # Build sets
    holiday_set = build_holiday_set()
    local_holiday_set = build_local_holiday_set()

    # ✅ Load the LabelEncoder for route
    route_encoder = load_route_encoder()
    if route_encoder is None:
        return JsonResponse({'error': 'Route encoder loading failed'}, status=500)

    try:
        route_code = route_encoder.transform([route])[0]
    except Exception as e:
        return JsonResponse({'error': f'Route encoding failed: {e}'}, status=500)


    # Semester flags
    semester_flags = get_historical_university_semester_flags(date_obj)

    # Build full feature set
    input_features = {
        'hour': hour,
        'route': route_code,
        'day_of_week': weekday,
        'is_holiday': is_any_holiday(date_obj, holiday_set, local_holiday_set),
        'is_friday': 1 if weekday == 4 else 0,
        'is_saturday': 1 if weekday == 5 else 0,
        'is_local_event': check_local_event_flag(date_obj),
        'is_others': check_others_event_flag(date_obj),
        'is_flagged': 0,
        'is_day_before_holiday': is_day_before_any_holiday(date_obj, holiday_set, local_holiday_set),
        'is_long_weekend': is_any_long_weekend(date_obj, holiday_set, local_holiday_set),
        'is_day_before_long_weekend': is_day_before_any_long_weekend(date_obj, holiday_set, local_holiday_set),
        'is_end_of_sem': semester_flags['is_end_of_sem'],
        'is_day_before_end_of_sem': semester_flags['is_day_before_end_of_sem'],
        'is_day_after_end_of_sem': semester_flags['is_day_after_end_of_sem'],
        'is_2days_after_end_of_sem': semester_flags['is_2days_after_end_of_sem'],
        'is_local_holiday': check_local_holiday_flag(date_obj),
        'is_start_of_sem': semester_flags['is_start_of_sem'],
        'is_week_after_end_of_sem': semester_flags['is_week_after_end_of_sem'],
        'is_week_before_end_of_sem': semester_flags['is_week_before_end_of_sem'],
        'is_within_ay': semester_flags['is_within_ay']
    }

    try:
        ordered_input = pd.DataFrame([[input_features[feature] for feature in features_to_use]], columns=features_to_use)
        predicted_commuters = model.predict(ordered_input)[0]
        predicted_commuters = round(predicted_commuters, 2)
        print(f"📍 Predicted commuters: {predicted_commuters}")
        return JsonResponse({'prediction': predicted_commuters})

    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return JsonResponse({'error': 'Prediction failed'}, status=500)

from datetime import datetime, timedelta
import pandas as pd
from django.http import JsonResponse

def rf_predict_commuters_2weeks(route, time_str, selected_date):
    model = load_pretrained_model()
    features_to_use = load_feature_list()
    
    if model is None or features_to_use is None:
        return JsonResponse({'error': 'Model or feature list loading failed'}, status=500)

    # Parse inputs
    try:
        start_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
        time_obj = datetime.strptime(time_str, "%I:%M%p").time()
    except ValueError:
        return JsonResponse({'error': 'Invalid date or time format'}, status=400)

    hour = time_obj.hour

    # Load helpers
    holiday_set = build_holiday_set()
    local_holiday_set = build_local_holiday_set()
    route_encoder = load_route_encoder()

    if route_encoder is None:
        return JsonResponse({'error': 'Route encoder loading failed'}, status=500)

    try:
        route_code = route_encoder.transform([route])[0]
    except Exception as e:
        return JsonResponse({'error': f'Route encoding failed: {e}'}, status=500)

    predictions = []

    for i in range(14):
        current_date = start_date + timedelta(days=i)
        weekday = current_date.weekday()

        semester_flags = get_historical_university_semester_flags(current_date)

        input_features = {
            'hour': hour,
            'route': route_code,
            'day_of_week': weekday,
            'is_holiday': is_any_holiday(current_date, holiday_set, local_holiday_set),
            'is_friday': 1 if weekday == 4 else 0,
            'is_saturday': 1 if weekday == 5 else 0,
            'is_local_event': check_local_event_flag(current_date),
            'is_others': check_others_event_flag(current_date),
            'is_flagged': 0,
            'is_day_before_holiday': is_day_before_any_holiday(current_date, holiday_set, local_holiday_set),
            'is_long_weekend': is_any_long_weekend(current_date, holiday_set, local_holiday_set),
            'is_day_before_long_weekend': is_day_before_any_long_weekend(current_date, holiday_set, local_holiday_set),
            'is_end_of_sem': semester_flags['is_end_of_sem'],
            'is_day_before_end_of_sem': semester_flags['is_day_before_end_of_sem'],
            'is_day_after_end_of_sem': semester_flags['is_day_after_end_of_sem'],
            'is_2days_after_end_of_sem': semester_flags['is_2days_after_end_of_sem'],
            'is_local_holiday': check_local_holiday_flag(current_date),
            'is_start_of_sem': semester_flags['is_start_of_sem'],
            'is_week_after_end_of_sem': semester_flags['is_week_after_end_of_sem'],
            'is_week_before_end_of_sem': semester_flags['is_week_before_end_of_sem'],
            'is_within_ay': semester_flags['is_within_ay']
        }

        try:
            ordered_input = pd.DataFrame([[input_features[feature] for feature in features_to_use]], columns=features_to_use)
            predicted_commuters = model.predict(ordered_input)[0]
            predicted_commuters = round(predicted_commuters, 2)
        except Exception as e:
            return JsonResponse({'error': f'Prediction failed on {current_date}: {e}'}, status=500)

        predictions.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'route': route,
            'time': time_str,
            'predicted_commuters': predicted_commuters
        })
        print(f"{current_date.strftime('%Y-%m-%d')} | Route: {route} | Time: {time_str} | Predicted: {predicted_commuters}")


    return JsonResponse({'predictions': predictions})

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

from datetime import datetime
#used in HistoricalDatasetUpload.html
def parse_date_strict(date_str):
    original = str(date_str).strip()
    print("Original:", original)

    # Remove time if it exists
    if " " in original:
        original = original.split(" ")[0]
        print(f"Stripped time: {original}")

    # Try special YYYY-DD-MM logic
    try:
        parts = original.split("-")
        if len(parts) == 3 and len(parts[0]) == 4:
            # Treat it as YYYY-DD-MM (flipped)
            flipped_str = f"{parts[2]}/{parts[1]}/{parts[0]}"  # MM/DD/YYYY
            parsed_date = datetime.strptime(flipped_str, "%m/%d/%Y")
            print("Assumed format: YYYY-DD-MM (flipped to MM/DD/YYYY)")
            print("Date in words:", parsed_date.strftime("%B %d, %Y"))
            print("Formatted as MM/DD/YYYY:", parsed_date.strftime("%m/%d/%Y"))
            return parsed_date.date()
    except Exception as e:
        print("Failed special YYYY-DD-MM interpretation:", e)

    # Try normal formats
    formats_to_try = [
        "%m/%d/%Y", "%Y-%m-%d", "%d-%m-%Y",
        "%d/%m/%Y", "%B %d, %Y", "%b %d, %Y", "%m-%d-%Y"
    ]

    for fmt in formats_to_try:
        try:
            parsed_date = datetime.strptime(original, fmt)
            # print(f"Successfully parsed using format '{fmt}'")
            # print("Date in words:", parsed_date.strftime("%B %d, %Y"))
            # print("Formatted as MM/DD/YYYY:", parsed_date.strftime("%m/%d/%Y"))
            return parsed_date.date()
        except ValueError:
            continue

    print(f"Could not parse: {original}")
    return None  # Explicit return if parsing fails

#-------------------------------------------------------------------------

from django.shortcuts import render, redirect
from django.http import JsonResponse
import pandas as pd
from .models import HistoricalDataset
from datetime import datetime

def historical_dataset_upload_list(request):
    
    if request.method == 'GET':
        return redirect('historical_dataset_upload_list')
    
    dataset_file = request.FILES.get('historical_dataset_file')
    force_upload = request.POST.get('force_upload') == 'true'

    if not dataset_file:
        return JsonResponse({'error': 'No file uploaded'}, status=400)

    file_extension = dataset_file.name.split('.')[-1]
    if file_extension == 'xlsx':
        df = pd.read_excel(dataset_file)
        
    elif file_extension == 'csv':
        df = pd.read_csv(dataset_file)
        
    else:
        return JsonResponse({'error': 'Unsupported file format'}, status=400)

    overlap_count = 0
    for _, row in df.iterrows():
        try:
            date_val = parse_date_strict(row['Date'])
            # date_val = pd.to_datetime(row['Date']).date()
           
            route = row['Route']
            time_val = datetime.strptime(row['Time'], "%I:%M %p").strftime("%H:%M")
        except Exception as e:
            print(f"Parsing error: {e}")
            continue

        # if HistoricalDataset.objects.filter(route=route, date=date_val, time=time_val).exists():
        #     overlap_count += 1

        #!
        existing_entries = HistoricalDataset.objects.filter(route=route, date=date_val, time=time_val)
        if existing_entries.exists():
            if force_upload:
                existing_entries.delete()  # Delete old entry before inserting new one
            else:
                overlap_count += 1



    # First check for overlaps — allow modal to trigger without saving anything
    if overlap_count > 0 and not force_upload:
        
        return JsonResponse({'overlap': True, 'count': overlap_count})


    # PROCEED WITH DATA UPLOAD
    user = request.user
    
    holiday_set = build_holiday_set()
    local_holiday_set = build_local_holiday_set()

    for _, row in df.iterrows():
        try:
            
            # date_val = pd.to_datetime(row['Date']).date()
            date_val = parse_date_strict(row['Date'])
            
        except Exception as e:
            print(f"Error parsing date: {e}")
            continue

        route = row['Route']
        try:
            time_val = datetime.strptime(row['Time'], "%I:%M %p").strftime("%H:%M")
        except ValueError as e:
            print(f"Error parsing time: {e}")
            continue

        num_commuters = row['Commuters']
        day_of_week = date_val.strftime("%A")
        month = date_val.strftime("%B")
        weekday = date_val.weekday()

        is_friday = weekday == 4
        is_saturday = weekday == 5

        is_holiday = is_any_holiday(date_val, holiday_set, local_holiday_set)

        is_day_before_holiday = is_day_before_any_holiday(date_val, holiday_set, local_holiday_set)
        is_long_weekend = is_any_long_weekend(date_val, holiday_set, local_holiday_set)
        is_day_before_long_weekend = is_day_before_any_long_weekend(date_val, holiday_set, local_holiday_set)


        is_local_holiday = check_local_holiday_flag(date_val)
        is_university_event = check_university_event_flag(date_val)
        is_local_event = check_local_event_flag(date_val)
        is_others = check_others_event_flag(date_val)

        semester_flags = get_historical_university_semester_flags(date_val)

        # Save to database
        HistoricalDataset.objects.create(
            date=date_val,
            route=route,
            time=time_val,
            num_commuters=num_commuters,
            user_code=user.user_code,
            filename=dataset_file.name,

            day_of_week=day_of_week,
            # day=date_val.strftime("%A"), 
            month=month,

            is_friday=is_friday,
            is_saturday=is_saturday,

            is_holiday=is_holiday,

            is_day_before_holiday=is_day_before_holiday,
            is_long_weekend=is_long_weekend,
            is_day_before_long_weekend=is_day_before_long_weekend,

            is_local_holiday=is_local_holiday,
            is_university_event=is_university_event,
            is_local_event=is_local_event,
            is_others=is_others,

            is_within_ay=semester_flags['is_within_ay'],
            is_start_of_sem=semester_flags['is_start_of_sem'],
            is_day_before_end_of_sem=semester_flags['is_day_before_end_of_sem'],
            is_week_before_end_of_sem=semester_flags['is_week_before_end_of_sem'],
            is_end_of_sem=semester_flags['is_end_of_sem'],
            is_day_after_end_of_sem=semester_flags['is_day_after_end_of_sem'],
            is_2days_after_end_of_sem=semester_flags['is_2days_after_end_of_sem'],
            is_week_after_end_of_sem=semester_flags['is_week_after_end_of_sem']
        )

    log_action(request, 'Historical Dataset Upload', f"User {user.first_name} {user.last_name} uploaded historical dataset.")

    return JsonResponse({'success': True})



from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import pandas as pd
from .models import HistoricalDataset
from .randomForest import train_random_forest_model
from datetime import datetime


def historical_dataset_export(request):
    """Exports the HistoricalDataset data to a CSV file."""
    print("Export function triggered!")  # Debug output

    # Get all dataset entries from HistoricalDataset model
    data = HistoricalDataset.objects.all().values()
    
    # Create DataFrame from queryset
    df = pd.DataFrame(list(data))

    if df.empty:
        print("No data available for export.")
        return HttpResponse("No data to export.", status=204)

    # Remove 'id' column (if it exists)
    df.drop(columns=['id'], inplace=True, errors='ignore')

    # Get current datetime for filename
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"historical_dataset_{now}.csv"

    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    df.to_csv(path_or_buf=response, index=False)

    print(f"Export successful! File sent: {filename}")
    return response


# views.py
from django.shortcuts import redirect
from django.contrib import messages
from .models import HistoricalDataset

def delete_all_historical_datasets(request):
    if request.method == "POST":
        HistoricalDataset.objects.all().delete()
        messages.success(request, "All historical datasets have been deleted.")
    return redirect('historical_dataset_event_list')  # Redirect back to the dataset list



import os
import glob
import joblib
from django.conf import settings
from django.utils.timezone import now
from .randomForest import train_random_forest_model
from .models import ModelTrainingHistory

from django.shortcuts import redirect
from django.contrib import messages

def train_random_forest_model_view(request):
    if request.method == 'POST':
        try:
            # Train model and get performance report
            model, performance_report = train_random_forest_model()

            #problem in adding the trained_by value so this is a proposed fix given that there will always be one object in the model
            latest_model = ModelTrainingHistory.objects.latest('trained_at')
            latest_model.trained_by = request.user.user_code
            latest_model.save(update_fields=["trained_by"])
            print("------------------------------------------------------Model trained by:", latest_model.trained_by)

            
            # Create unique timestamp-based filename
            timestamp = now().strftime('%Y%m%d_%H%M%S')
            base_filename = f"random_forest_model_{timestamp}"

            # Directory to save model and report
            output_dir = os.path.join(settings.MEDIA_ROOT, 'ml_models')
            os.makedirs(output_dir, exist_ok=True)

            # Remove previous .pkl and .txt files
            for ext in ('*.pkl', '*.txt'):
                for old_file in glob.glob(os.path.join(output_dir, ext)):
                    os.remove(old_file)

            # Save model
            model_path = os.path.join(output_dir, f"{base_filename}.pkl")
            joblib.dump(model, model_path)

            # Save report as a string (avoids TypeError)
            report_path = os.path.join(output_dir, f"{base_filename}.txt")
            with open(report_path, 'w') as f:
                f.write(str(performance_report))  # Ensures it’s a string

            # Success message
            messages.success(request, "Model trained successfully and saved!")

            return redirect('historical_dataset_event_list')
            
    
        except Exception as e:
            
            # messages.error(request, f"Error during model training: {str(e)}")
            return redirect('historical_dataset_upload_list')

    return JsonResponse({'error': 'Invalid request method'}, status=405)


#-------------------------------------------------------------------------

def historical_dataset_event_list(request):
    # Load data
    datasets = HistoricalDataset.objects.all().order_by('-id')
    recent_events = TemporalEvent.objects.all().order_by('event_type', 'sort_order')
    holidays = HolidayEvent.objects.all().order_by('date')
    events = HistoricalTemporalEvent.objects.all().order_by('-date')

    has_missing_dates = recent_events.filter(date__isnull=True).exists()
    is_event_list_empty = not datasets.exists()
    can_train_model = not has_missing_dates and not is_event_list_empty


    user_map = {user.user_code: user for user in User.objects.all()}

    for event in events:
        event.created_by_user = user_map.get(event.created_by)
        event.updated_by_user = user_map.get(event.updated_by)

    for event in recent_events:
        event.created_by_user = user_map.get(event.created_by)
        event.updated_by_user = user_map.get(event.updated_by)

    context = {
        'historical_datasets': datasets,
        'recent_events': recent_events,
        'holidays': holidays,
        'historical_events': events,

        'has_missing_dates': has_missing_dates,
        'is_event_list_empty': is_event_list_empty,
        'can_train_model': can_train_model,

        "has_historical_data": HistoricalDataset.objects.exists(),
    }

    # print("has_missing_dates:", has_missing_dates)
    # print("is_event_list_empty:", is_event_list_empty)
    # print("can_train_model:", can_train_model)

    return render(request, 'admin/historicalDatasetUpload.html', context)


def add_historical_event(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("📩 Received historical event data:", data)

            event_name = data.get('event_name', '').strip()
            event_type = data.get('event_type', '')
            event_date = data.get('date', None)

            if event_type not in dict(TemporalEvent.EVENT_TYPE_CHOICES):
                return JsonResponse({'status': 'error', 'message': 'Invalid event type.'}, status=400)

            if HistoricalTemporalEvent.objects.filter(event_name=event_name, date=event_date).exists():                         # can be improved filter for similar looking event inputs
                return JsonResponse({'status': 'error', 'message': 'Event already exists.'}, status=400)

            created_by_user = request.user.user_code

            HistoricalTemporalEvent.objects.create(
                event_name=event_name,
                event_type=event_type,
                date=event_date,
                created_by=created_by_user,
                updated_by=created_by_user,
            )

            log_action(request, 'Add Historical Event', f"{event_name} added by {request.user.first_name} {request.user.last_name}.")
            return JsonResponse({'status': 'success'}, status=201)

        except Exception as e:
            logger.error(f"❌ Error adding historical event: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Server error.'}, status=500)


from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json

User = get_user_model()

def edit_historical_event(request):
    print("Edit historical event view triggered!") 
    if request.method == "POST":
        try:
            # Parse incoming data
            data = json.loads(request.body)
            event_code = data.get("event_code")  # Get the event code to identify the event
            event = get_object_or_404(HistoricalTemporalEvent, event_code=event_code)  # Find event by event_code

            # Capture the logged-in user's UUID
            updated_by = request.user.user_code  # Assuming your user model has `user_code` field

            # Log the action
            log_action(request, 'Edit Historical Event', f"Historical event {event.event_name} update requested.")

            # Debug print
            print(f"Received data to update historical event: {data}")

            # Update fields
            event.event_name = data["event_name"]
            event.event_type = data["event_type"]
            event.date = data["date"]
            event.updated_by = updated_by
            
            # Save changes
            event.save()

            log_action(request, 'Edit Historical Event', f"Historical event {event.event_name} edited by {request.user.first_name} {request.user.last_name}.")
            print(f"Updated historical event: {event.event_name}, {event.event_type}, {event.date}, updated by: {event.updated_by}")

            return JsonResponse({'status': 'success'})              #!! removed alert

        except Exception as e:
            print(f"Error editing historical event: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from .models import HistoricalTemporalEvent  # ✅ Correct model

User = get_user_model()

# @csrf_exempt
def delete_historical_event(request):
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            event_code = data.get("event_code")

            print(f"historicalDataset...Received event code to delete: {event_code}")
            if not event_code:
                return JsonResponse({'status': 'error', 'message': 'Event code is required.'}, status=400)

            event = get_object_or_404(HistoricalTemporalEvent, event_code=event_code)  # ✅ Correct model usage

            log_action(request, 'Delete Historical Event', f"Event {event.event_name} deleted by {request.user.first_name} {request.user.last_name}.")  # Optional: customize log

            event.delete()

            print(f"✅ Deleted historical event with code: {event_code}")
            return JsonResponse({'status': 'success', 'message': 'Historical event deleted successfully'})

        except Exception as e:
            print(f"❌ Error deleting historical event: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def group_semester_dates_historical():
    grouped_dates = {
        'Start of 1st Sem': [],
        'End of 1st Sem': [],
        'Start of 2nd Sem': [],
        'End of 2nd Sem': [],
        'Start of Midyear': [],
        'End of Midyear': [],
        'Start of 1st Sem Final Examinations': [],
        'End of 1st Sem Final Examinations': [],
        'Start of 2nd Sem Final Examinations': [],
        'End of 2nd Sem Final Examinations': [],
        'Start of Mid Year Final Examinations': [],
        'End of Mid Year Final Examinations': []
    }

    # Fetch all university_event type events
    events = HistoricalTemporalEvent.objects.filter(event_type='university_event')

    for event in events:
        normalized_name = event.event_name.strip().upper()  # Normalize case
        for key in grouped_dates:
            if key.upper() in normalized_name:
                grouped_dates[key].append(event.date)

    return grouped_dates


from datetime import timedelta

def get_historical_university_semester_flags(target_date):
    flags = {
        'is_within_ay': False,
        'is_start_of_sem': False,
        'is_day_before_end_of_sem': False,
        'is_week_before_end_of_sem': False,
        'is_end_of_sem': False,
        'is_day_after_end_of_sem': False,
        'is_2days_after_end_of_sem': False,
        'is_week_after_end_of_sem': False
    }

    grouped = group_semester_dates_historical()  # dynamically fetches data

    semester_ranges = [
        ('Start of 1st Sem', 'End of 1st Sem'),
        ('Start of 2nd Sem', 'End of 2nd Sem'),
        ('Start of Midyear', 'End of Midyear'),
    ]

    for start_key, end_key in semester_ranges:
        start_dates = grouped.get(start_key, [])
        end_dates = grouped.get(end_key, [])

        for start_date, end_date in zip(start_dates, end_dates):
            if start_date <= target_date <= end_date:
                flags['is_within_ay'] = True
            if target_date == start_date:
                flags['is_start_of_sem'] = True
            if target_date == end_date - timedelta(days=1):
                flags['is_day_before_end_of_sem'] = True
            if end_date - timedelta(days=7) <= target_date < end_date:
                flags['is_week_before_end_of_sem'] = True
            if target_date == end_date:
                flags['is_end_of_sem'] = True
            if target_date == end_date + timedelta(days=1):
                flags['is_day_after_end_of_sem'] = True
            if target_date == end_date + timedelta(days=2):
                flags['is_2days_after_end_of_sem'] = True
            if end_date < target_date <= end_date + timedelta(days=7):
                flags['is_week_after_end_of_sem'] = True

    return flags

#-------------------------------------------------------------------------


#-------------------------------------------------------------------------

# Dashboard
from django.shortcuts import render
from datetime import datetime, timedelta

def dashboard(request):
    # upcoming_events_view(request)
    ##MODIFY THIS LATER BUT CANNOT REMOVE THESE TEMP VALUES YET
    # Placeholder values – replace these with real queries later
    # avg_commuters = 1200
    # rf_prediction = 1280

    # # Generate mock 2-week predictions
    # today = datetime.now().date()
    # predictions = []
    # for i in range(14):
    #     date = today + timedelta(days=i)
    #     predictions.append({
    #         'date': date.strftime('%Y-%m-%d'),
    #         'route': 'A to B' if i % 2 == 0 else 'A to C',
    #         'time': '07:00 AM',
    #         'predicted_commuters': 100 + i * 10  # dummy numbers
    #     })

    context = {
        'test': None
    }

    # return render(request, 'admin/dashboard.html', context)
    return render(request, 'admin/dashboard.html', context)


#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

from django.http import JsonResponse
from .models import HistoricalDataset
from django.db.models import Sum
from collections import OrderedDict

def monthly_commuter_stats(request):
    qs = HistoricalDataset.objects.order_by("-date").values_list("date", flat=True)

    seen = set()
    recent_months = []

    for date in qs:
        year_month = (date.year, date.month)
        if year_month not in seen:
            seen.add(year_month)
            recent_months.append(year_month)
        if len(recent_months) == 5:  # Now need 5 for comparison
            break

    recent_months = sorted(recent_months)

    labels = []
    data = []

    month_data = {}

    for year, month in recent_months:
        count = HistoricalDataset.objects.filter(
            date__year=year, date__month=month
        ).aggregate(total=Sum("num_commuters"))["total"] or 0

        label = f"{datetime(year, month, 1).strftime('%b %Y')}"
        labels.append(label)
        data.append(count)
        month_data[(year, month)] = count

    current = recent_months[-1]
    previous = recent_months[-2] if len(recent_months) > 1 else None

    current_count = month_data.get(current, 0)
    prev_count = month_data.get(previous, 0)

    # Compute percentage change
    if prev_count > 0:
        change_percent = round(((current_count - prev_count) / prev_count) * 100, 2)
    else:
        change_percent = 0

    return JsonResponse({
        "labels": labels,
        "data": data,
        "current_month_count": current_count,
        "current_month_name": f"{datetime(*current, 1).strftime('%b %Y')}",
        "change_percent": change_percent
    })



from django.http import JsonResponse
from django.db.models import Sum, Max
from .models import HistoricalDataset
import calendar

def route_commuter_percentages(request):
    print("✅ Route commuter percentages view called")

    # Get the latest available date in the dataset
    latest_date = HistoricalDataset.objects.aggregate(latest=Max('date'))['latest']
    if not latest_date:
        print("⚠️ No data in HistoricalDataset")
        return JsonResponse({
            "labels": [],
            "data": []
        })

    # Determine the first and last day of the latest month
    year = latest_date.year
    month = latest_date.month
    start_date = latest_date.replace(day=1)
    last_day = calendar.monthrange(year, month)[1]
    end_date = latest_date.replace(day=last_day)

    print(f"📅 Filtering for month: {year}-{month:02d} ({start_date} to {end_date})")

    # Get total commuters per route for that month
    route_counts = (
        HistoricalDataset.objects
        .filter(date__range=(start_date, end_date))
        .values("route")
        .annotate(total_commuters=Sum("num_commuters"))
        .order_by("-total_commuters")
    )

    labels = [entry["route"] for entry in route_counts]
    data = [entry["total_commuters"] for entry in route_counts]

    print(f"📊 Routes: {labels}")
    print(f"👥 Totals: {data}")

    return JsonResponse({
        "labels": labels,
        "data": data
    })


from django.http import JsonResponse
from django.db.models import Sum, Max
from datetime import timedelta
from .models import HistoricalDataset  # Adjust import as needed

def top_commuter_times(request):
    # Get the latest date in the dataset
    latest_date = HistoricalDataset.objects.aggregate(latest=Max('date'))['latest']
    if not latest_date:
        return JsonResponse({"labels": [], "data": []})

    # Get the first day of that month
    first_day_of_month = latest_date.replace(day=1)

    # Aggregate total commuters by time for the latest month
    time_counts = (
        HistoricalDataset.objects
        .filter(date__range=(first_day_of_month, latest_date))
        .values('time')
        .annotate(total_commuters=Sum('num_commuters'))
        .order_by('-total_commuters')[:3]  # top 3 times
    )

    labels = [entry['time'] for entry in time_counts]
    data = [entry['total_commuters'] for entry in time_counts]

    return JsonResponse({
        'labels': labels,
        'data': data,
    })



from django.http import JsonResponse
from django.db.models import Sum
from django.db.models.functions import TruncDate
from .models import HistoricalDataset
from datetime import timedelta

def commuters_heatmap_data(request):
    # Get the most recent date in the dataset
    latest_entry = HistoricalDataset.objects.order_by('-date').first()
    if not latest_entry:
        return JsonResponse({'dates': [], 'counts': [], 'flags': {}})

    latest_date = latest_entry.date
    month_start = latest_date.replace(day=1)
    next_month = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1)

    # Aggregate commuter counts
    daily_totals = (
        HistoricalDataset.objects
        .filter(date__gte=month_start, date__lt=next_month)
        .annotate(day=TruncDate('date'))
        .values('day')
        .annotate(total=Sum('num_commuters'))
        .order_by('day')
    )
    daily_dict = {entry['day']: entry['total'] for entry in daily_totals}

    # Build complete data
    current_day = month_start
    full_dates = []
    full_counts = []
    flags_dict = {}

    while current_day < next_month:
        full_dates.append(current_day.isoformat())
        full_counts.append(daily_dict.get(current_day, 0))

        # Fetch the first dataset entry for that day
        ds = HistoricalDataset.objects.filter(date=current_day).first()
        if ds:
            flags_dict[current_day.isoformat()] = {
                'is_holiday': ds.is_holiday,
                'is_friday': ds.is_friday,
                'is_saturday': ds.is_saturday,
                'is_day_before_holiday': ds.is_day_before_holiday,
                'is_long_weekend': ds.is_long_weekend,
                'is_day_before_long_weekend': ds.is_day_before_long_weekend,
                'is_local_holiday': ds.is_local_holiday,
                'is_university_event': ds.is_university_event,
                'is_local_event': ds.is_local_event,
                'is_others': ds.is_others,
                'is_flagged': ds.is_flagged,
                'is_within_ay': ds.is_within_ay,
                'is_start_of_sem': ds.is_start_of_sem,
                'is_day_before_end_of_sem': ds.is_day_before_end_of_sem,
                'is_week_before_end_of_sem': ds.is_week_before_end_of_sem,
                'is_end_of_sem': ds.is_end_of_sem,
                'is_day_after_end_of_sem': ds.is_day_after_end_of_sem,
                'is_2days_after_end_of_sem': ds.is_2days_after_end_of_sem,
                'is_week_after_end_of_sem': ds.is_week_after_end_of_sem
            }
        else:
            flags_dict[current_day.isoformat()] = {}

        current_day += timedelta(days=1)

    return JsonResponse({
        'dates': full_dates,
        'counts': full_counts,
        'flags': flags_dict
    })


from django.http import JsonResponse
from django.db.models import Sum
from django.db.models.functions import TruncDate
from datetime import timedelta
from .models import HistoricalDataset

def daily_commuter_trend(request):
    latest_entry = HistoricalDataset.objects.order_by('-date').first()
    if not latest_entry:
        return JsonResponse({"labels": [], "data": []})

    latest_date = latest_entry.date
    start_date = latest_date - timedelta(days=29)

    daily_data = (
        HistoricalDataset.objects
        .filter(date__range=(start_date, latest_date))
        .annotate(day=TruncDate('date'))
        .values('day')
        .annotate(total_commuters=Sum('num_commuters'))
        .order_by('day')
    )

    labels = [entry['day'].strftime('%b %d') for entry in daily_data]
    data = [entry['total_commuters'] for entry in daily_data]

    return JsonResponse({
        "labels": labels,
        "data": data
    })



from collections import defaultdict
from django.db.models.functions import TruncDate
from django.db.models import Sum
from datetime import timedelta

def daily_commuter_trend_per_route(request):
    latest_entry = HistoricalDataset.objects.order_by('-date').first()
    if not latest_entry:
        return JsonResponse({"labels": [], "routes": [], "datasets": {}})

    latest_date = latest_entry.date
    start_date = latest_date - timedelta(days=29)

    # Query daily totals grouped by day and route
    qs = (
        HistoricalDataset.objects
        .filter(date__range=(start_date, latest_date))
        .annotate(day=TruncDate('date'))
        .values('day', 'route')
        .annotate(total_commuters=Sum('num_commuters'))
        .order_by('day')
    )

    # Get all unique dates and routes
    dates = sorted({entry['day'] for entry in qs})
    routes = sorted({entry['route'] for entry in qs})

    # Initialize dictionary: {route: [0, 0, ...]} with length = number of dates
    route_data = {route: [0]*len(dates) for route in routes}

    # Map each date to its index for quick filling
    date_index = {date: idx for idx, date in enumerate(dates)}

    # Fill the commuter counts per route and date
    for entry in qs:
        idx = date_index[entry['day']]
        route_data[entry['route']][idx] = entry['total_commuters']

    # Format dates for labels
    labels = [date.strftime('%b %d') for date in dates]

    return JsonResponse({
        "labels": labels,
        "routes": routes,
        "datasets": route_data
    })


from django.http import JsonResponse
from django.db.models import Sum
from django.db.models.functions import TruncDate
from datetime import timedelta
from collections import defaultdict
from .models import HistoricalDataset

def daily_commuter_trend_per_time(request):
    latest_entry = HistoricalDataset.objects.order_by('-date').first()
    if not latest_entry:
        return JsonResponse({"labels": [], "times": [], "datasets": {}})

    latest_date = latest_entry.date
    start_date = latest_date - timedelta(days=29)

    # Group by date and time
    qs = (
        HistoricalDataset.objects
        .filter(date__range=(start_date, latest_date))
        .annotate(day=TruncDate('date'))
        .values('day', 'time')
        .annotate(total_commuters=Sum('num_commuters'))
        .order_by('day')
    )

    # Extract unique dates and time strings
    dates = sorted({entry['day'] for entry in qs})
    times = sorted({entry['time'].strftime('%H:%M') for entry in qs})

    # Build index map for dates
    date_index = {date: i for i, date in enumerate(dates)}
    time_data = {time: [0] * len(dates) for time in times}

    # Fill commuter counts
    for entry in qs:
        idx = date_index[entry['day']]
        time_str = entry['time'].strftime('%H:%M')
        time_data[time_str][idx] = entry['total_commuters']

    labels = [d.strftime('%b %d') for d in dates]

    return JsonResponse({
        "labels": labels,
        "times": times,
        "datasets": time_data
    })


from django.http import JsonResponse
from django.utils.timezone import now
from .models import ModelTrainingHistory

from datetime import timezone

from .models import CustomUser 


from django.http import JsonResponse
from .models import ModelTrainingHistory, CustomUser
from datetime import datetime

def get_latest_model_info(request):
    latest_model = ModelTrainingHistory.objects.order_by('-trained_at').first()

    # upcoming_events_view(request)                                                               #!!!!

    if not latest_model:
        return JsonResponse({'error': 'No model found'})

    try:
        user = CustomUser.objects.get(user_code=latest_model.trained_by)
        trained_by_name = f"{user.first_name} {user.last_name}"
    except CustomUser.DoesNotExist:
        trained_by_name = "Unknown"

    days_since_training = (datetime.now().date() - latest_model.trained_at.date()).days

    return JsonResponse({
        'model_name': latest_model.model_name,
        'trained_by': trained_by_name,
        'trained_at': latest_model.trained_at.strftime("%Y-%m-%d %H:%M:%S"),
        'days_since_training': days_since_training,
        'rmse': latest_model.rmse,
        'mae': latest_model.mae
    })


# from django.http import JsonResponse
# from datetime import date, timedelta
# from .models import HolidayEvent, TemporalEvent

def upcoming_events_view(request):
    events = []
    # today = date.today()
    
    today = date(2024, 12, 20)
    thirty_days_later = today + timedelta(days=30)
    print("---------------------------------------------------Upcoming events view called")

    print(f"[INFO] Today: {today}")
    print(f"[INFO] 30 Days Later: {thirty_days_later}")

    temporal_events = TemporalEvent.objects.filter(date__range=(today, thirty_days_later))
    # holiday_events = HolidayEvent.objects.filter(date__range=(today, thirty_days_later))
    holiday_events = HolidayEvent.objects.all()

    # temporal_events = TemporalEvent.objects.all()
    # holiday_events = HolidayEvent.objects.all()

    
    print(f"[INFO] Found {temporal_events.count()} temporal events")
    print(f"[INFO] Found {holiday_events.count()} holiday events")


    #---------------------------------------------------------------------------
    date_range_md = set()
    current_date = today
    while current_date <= thirty_days_later:
        date_range_md.add(current_date.strftime('%m-%d'))
        current_date += timedelta(days=1)

    # Then, filter holidays
    for h in holiday_events:
        md = h.date.strftime('%m-%d')
        if md in date_range_md:
            # print(f"[HOLIDAY] {h.date}: {h.event_type} - {h.event_name}")
            events.append({
                'name': h.event_name,   
                'type': h.event_type, 
                'date': h.date.strftime('%Y-%m-%d'),
            })
    #---------------------------------------------------------------------------

    for e in temporal_events:
        # print(f"[TEMPORAL] {e.date}: {e.event_type} - {e.event_name}")
        events.append({
            'name': e.event_name,  
            'type': e.event_type,
            'date': e.date.strftime('%Y-%m-%d'),
            
            
        })

    
    # After appending holidays and temporal events...

    print("[INFO] Combined events:")
    for event in events:
        # print(f"{event['date']} - {event['type']} - {event['name']}")
        print(f"{{'name': '{event['name']}', 'type': '{event['type']}', 'date': '{event['date']}'}},")
    
    print("---------------------------------------------------Upcoming events view called")

    return JsonResponse({'data': events})





#-------------------------------------------------------------------------
#-------------------------------------------------------------------------