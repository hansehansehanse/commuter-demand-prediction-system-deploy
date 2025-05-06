
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





#-------------------------------------------------------------------------

#-------------------------------------------------------------------------

from datetime import timedelta, date
from CommuterDemandPredictionSystem.models import HolidayEvent, TemporalEvent

def build_holiday_set():
    holidays = set()
    # Yearless holidays
    for h in HolidayEvent.objects.all():
        for year in range(2000, 2101):  # safe test range
            holidays.add(date(year, h.date.month, h.date.day))
    # Dated temporal events
    for t in TemporalEvent.objects.exclude(date=None):
        holidays.add(t.date)
    return holidays

def is_day_before_holiday(d, holidays):
    return (d + timedelta(days=1)) in holidays

def is_long_weekend(d, holidays):
    return (
        (d.weekday() == 4 and (d + timedelta(days=1)) in holidays and (d + timedelta(days=2)).weekday() == 6) or
        (d.weekday() == 5 and (d + timedelta(days=2)) in holidays) or
        (d.weekday() == 6 and (d - timedelta(days=2)) in holidays)
    )

def is_day_before_long_weekend(d, holidays):
    return is_long_weekend(d + timedelta(days=1), holidays)

#-------------------------------------------------------------------------


def check_local_holiday_flag(target_date):
    return TemporalEvent.objects.filter(date=target_date, event_type='local_holiday').exists()

def check_university_event_flag(target_date):
    return TemporalEvent.objects.filter(date=target_date, event_type='university_event').exists()

def check_local_event_flag(target_date):
    return TemporalEvent.objects.filter(date=target_date, event_type='local_event').exists()

def check_others_event_flag(target_date):
    return TemporalEvent.objects.filter(date=target_date, event_type='others').exists()


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

    # Collect start and end dates of sems
    events = TemporalEvent.objects.filter(event_type='university_event')
    sem_starts = events.filter(event_name__icontains='Start of').order_by('date')
    sem_ends = events.filter(event_name__icontains='End of').order_by('date')

    for start_event, end_event in zip(sem_starts, sem_ends):
        start_date = start_event.date
        end_date = end_event.date

        if start_date <= target_date <= end_date:
            flags['is_within_ay'] = True
        if target_date == start_date:
            flags['is_start_of_sem'] = True
        if target_date == end_date - timedelta(days=1):
            flags['is_day_before_end_of_sem'] = True

        # if target_date == end_date - timedelta(days=7):
        #     flags['is_week_before_end_of_sem'] = True
        if end_date - timedelta(days=7) <= target_date < end_date:                      # 7 days before eos
            flags['is_week_before_end_of_sem'] = True


        if target_date == end_date:
            flags['is_end_of_sem'] = True
        if target_date == end_date + timedelta(days=1):
            flags['is_day_after_end_of_sem'] = True
        if target_date == end_date + timedelta(days=2):
            flags['is_2days_after_end_of_sem'] = True
        # if target_date == end_date + timedelta(days=7):
        #     flags['is_week_after_end_of_sem'] = True
        if end_date < target_date <= end_date + timedelta(days=7):                      # 7 days after eos
            flags['is_week_after_end_of_sem'] = True

    return flags


#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

# #admin
# def cdps_admin_accountManagement(request):
#     # context = {'sidebar_items':emp_sidebar_items}
#     context = {}
#     return render(request, 'admin/accountManagement.html', context)

# def cdps_admin_actionLog(request):
#     # context = {'sidebar_items':emp_sidebar_items}
#     context = {}
#     return render(request, 'admin/actionLog.html', context)


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
                    return redirect(reverse('account_management'))
                
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

from django.contrib.auth import get_user_model
from .models import Dataset, HolidayEvent, TemporalEvent
import pandas as pd
from datetime import datetime
from django.shortcuts import render, redirect

User = get_user_model()

def dataset_upload_list(request):
    if request.method == 'POST':
        dataset_file = request.FILES.get('dataset_file')
        if dataset_file:
            file_extension = dataset_file.name.split('.')[-1]
            if file_extension == 'xlsx':
                df = pd.read_excel(dataset_file)
            elif file_extension == 'csv':
                df = pd.read_csv(dataset_file)

            user = request.user
            # print(f"User Code: {user.user_code}")  # Debug

            holidays = build_holiday_set()  # Build once

            for _, row in df.iterrows():
                try:
                    date_val = pd.to_datetime(row['Date']).date()
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
                is_holiday = date_val in holidays
                is_before_holiday = is_day_before_holiday(date_val, holidays)
                is_lweekend = is_long_weekend(date_val, holidays)
                is_before_lweekend = is_day_before_long_weekend(date_val, holidays)

                is_local_holiday = check_local_holiday_flag(date_val)
                is_university_event = check_university_event_flag(date_val)
                is_local_event = check_local_event_flag(date_val)
                is_others = check_others_event_flag(date_val)

                semester_flags = get_university_semester_flags(date_val)

                is_within_ay = semester_flags['is_within_ay']
                is_start_of_sem = semester_flags['is_start_of_sem']
                is_day_before_end_of_sem = semester_flags['is_day_before_end_of_sem']
                is_week_before_end_of_sem = semester_flags['is_week_before_end_of_sem']
                is_end_of_sem = semester_flags['is_end_of_sem']
                is_day_after_end_of_sem = semester_flags['is_day_after_end_of_sem']
                is_2days_after_end_of_sem = semester_flags['is_2days_after_end_of_sem']
                is_week_after_end_of_sem = semester_flags['is_week_after_end_of_sem']


                # print(
                #     f"Date: {date_val} | "
                #     f"is_within_ay: {is_within_ay}, "
                #     f"is_start_of_sem: {is_start_of_sem}, "
                #     f"is_day_before_end_of_sem: {is_day_before_end_of_sem}, "
                #     f"is_week_before_end_of_sem: {is_week_before_end_of_sem}, "
                #     # f"is_end_of_sem: {is_end_of_sem}, "
                #     # f"is_day_after_end_of_sem: {is_day_after_end_of_sem}, "
                #     # f"is_2days_after_end_of_sem: {is_2days_after_end_of_sem}, "
                #     # f"is_week_after_end_of_sem: {is_week_after_end_of_sem}"
                # )

                # print(
                #     f"Date: {date_val} | "
                #     # f"is_within_ay: {is_within_ay}, "
                #     # f"is_start_of_sem: {is_start_of_sem}, "
                #     # f"is_day_before_end_of_sem: {is_day_before_end_of_sem}, "
                #     # f"is_week_before_end_of_sem: {is_week_before_end_of_sem}, "
                #     f"is_end_of_sem: {is_end_of_sem}, "
                #     f"is_day_after_end_of_sem: {is_day_after_end_of_sem}, "
                #     f"is_2days_after_end_of_sem: {is_2days_after_end_of_sem}, "
                #     f"is_week_after_end_of_sem: {is_week_after_end_of_sem}"
                # )


                Dataset.objects.create(
                    date=date_val,
                    route=route,
                    time=time_val,
                    num_commuters=num_commuters,
                    user_code=user.user_code,
                    filename=dataset_file.name,

                    day=day_of_week,
                    month=month,
                    is_friday=is_friday,
                    is_saturday=is_saturday,
                    is_holiday=is_holiday,
                    is_day_before_holiday=is_before_holiday,
                    is_long_weekend=is_lweekend,
                    is_day_before_long_weekend=is_before_lweekend,

                    # Temporal event flags
                    is_local_holiday=is_local_holiday,
                    is_university_event=is_university_event,
                    is_local_event=is_local_event,
                    is_others=is_others,

                    # Semester-related flags
                    is_within_ay=is_within_ay,
                    is_start_of_sem=is_start_of_sem,
                    is_day_before_end_of_sem=is_day_before_end_of_sem,
                    is_week_before_end_of_sem=is_week_before_end_of_sem,
                    is_end_of_sem=is_end_of_sem,
                    is_day_after_end_of_sem=is_day_after_end_of_sem,
                    is_2days_after_end_of_sem=is_2days_after_end_of_sem,
                    is_week_after_end_of_sem=is_week_after_end_of_sem
                )

                log_action(request, 'Dataset Upload', f"User {user.first_name} {user.last_name} upload dataset.")


            return redirect('dataset_upload_list')

    datasets = Dataset.objects.all()

    user_map = {
        u.user_code: u for u in User.objects.filter(user_code__in=[d.user_code for d in datasets])
    }

    for d in datasets:
        d.uploader = user_map.get(d.user_code)

    return render(request, 'admin/datasetUpload.html', {'datasets': datasets})

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
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
#-------------------------------------------------------------------------

from django.shortcuts import render
from .cdps import train_and_predict_random_forest

def predict_commuters(request):
    # Get the predictions for the next 2 weeks
    predictions = train_and_predict_random_forest()

    # Render the predictions in the table format
    return render(request, 'admin/datasetPrediction.html', {'predictions': predictions})




#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
from django.shortcuts import render
from django.db.models import Avg
from .models import Dataset
import json

from django.http import JsonResponse
from django.db.models import Sum
from .models import Dataset



def dataset_graph_data(request):
    print("✅ dataset_graph_data called")

    recent_dates = Dataset.objects.values_list('date', flat=True).distinct().order_by('-date')[:7]
    data = Dataset.objects.filter(date__in=recent_dates).values('date', 'route', 'time').annotate(
        total_commuters=Sum('num_commuters')
    ).order_by('date', 'route', 'time')
    return JsonResponse(list(data), safe=False)


#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

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
            return ajax_random_forest_prediction(route, time_str, selected_date)


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
from .models import Dataset
import json

def get_last_7_records_chart_data(route, time_str):
    try:
        time_obj = datetime.strptime(time_str, "%I:%M%p").time()
    except ValueError:
        return JsonResponse({'error': 'Invalid time format'})

    # Get the latest 7 historical entries for that route & time
    results = Dataset.objects.filter(route=route, time=time_obj).order_by('-date')[:7]
    results = sorted(results, key=lambda x: x.date)  # Ascending order for the chart

    dates = [r.date.strftime('%Y-%m-%d') for r in results]
    num_commuters = [r.num_commuters for r in results]

    chart_data = {
        'dates': dates,
        'num_commuters': num_commuters,
    }
    # print("get_last_7_records_chart_data")
    return JsonResponse({'chart_data': json.dumps(chart_data)})


from .models import Dataset
from django.db.models import Avg
from datetime import datetime
from django.http import JsonResponse

def get_average_commuters_from_date(route, time_str, selected_date):
    
    try:
        # Parse inputs
        date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
        time_obj = datetime.strptime(time_str, "%I:%M%p").time()  # 12hr to 24hr

        # Try to find the latest available date on or before the selected date
        latest_available = Dataset.objects.filter(
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
        matching_records = Dataset.objects.filter(
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


from django.http import JsonResponse
from .pm_rf_single import train_and_predict_random_forest_single  # Make sure to import your function

def ajax_random_forest_prediction(route, time_str, selected_date):
    print("ajax_random_forest_prediction")
    try:
        date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
        time_obj = datetime.strptime(time_str, "%I:%M%p").time()  # 12hr to 24hr

        prediction = train_and_predict_random_forest_single(route, time_obj, date_obj)
        print(f"Prediction for {route} at {time_str} on {selected_date}: {prediction}")

        return JsonResponse({'prediction': round(prediction, 2)})

    except Exception as e:
        print(f"Prediction Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)

       
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------







