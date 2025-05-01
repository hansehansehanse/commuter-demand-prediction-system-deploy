
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import make_password

from .models import CustomUser

import json
import uuid

import logging

from .models import ActionLog  # Assuming log_action uses the ActionLog model.


emp_sidebar_items = [
    {'url':'hris_emp_dashboard', 'icon_class':'ti-smart-home', 'name':'Dashboard'},
    {'url':'hris_emp_records', 'icon_class':'ti-file', 'name':'Records'},
    {'url':'hris_emp_payroll', 'icon_class':'ti-file-dollar', 'name':'Payroll'},
    {'url':'hris_emp_leaves', 'icon_class':'ti-checkbox', 'name':'Leaves'},
]


#-------------------------------------------------------------------------
# def cdps_admin_dashboard(request):
#     # context = {'sidebar_items':emp_sidebar_items}
#     context = {}
#     return render(request, 'admin/dashboard.html', context)

# def cdps_admin_dashboard2(request):
#     # context = {'sidebar_items':emp_sidebar_items}
#     context = {}
#     return render(request, 'admin/dashboard2.html', context)

#-------------------------------------------------------------------------
#admin
def cdps_admin_accountManagement(request):
    # context = {'sidebar_items':emp_sidebar_items}
    context = {}
    return render(request, 'admin/accountManagement.html', context)

def cdps_admin_actionLog(request):
    # context = {'sidebar_items':emp_sidebar_items}
    context = {}
    return render(request, 'admin/actionLog.html', context)


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


            # log_action(user, 'Add User', f"User {user.first_name} {user.last_name} was added.")
            # Pass request.user to log_action
            log_action(request, 'Add User', f"User {user.first_name} {user.last_name} account added.")

            # log_action(request, 'Login', f"User {user.first_name} {user.last_name} logged in.")

            return JsonResponse({'status': 'success'}, status=201)

        except Exception as e:
            print("❌ Exception:", e)
            logger.error(f"Error adding user: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Error occurred while adding user.'}, status=500)


#-------------------------------------------------------------------------
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .models import CustomUser
# from django.contrib.auth.hashers import make_password

# @csrf_exempt  # only if you test without csrf token; otherwise keep csrf protection
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
from .models import Dataset
import pandas as pd
from datetime import datetime
from django.shortcuts import render, redirect

User = get_user_model()

def dataset_upload_list(request):
    if request.method == 'POST':
        dataset_file = request.FILES.get('dataset_file')
        if dataset_file:
            # Read the dataset using pandas
            file_extension = dataset_file.name.split('.')[-1]
            if file_extension == 'xlsx':
                df = pd.read_excel(dataset_file)
            elif file_extension == 'csv':
                df = pd.read_csv(dataset_file)

            print(df.head())  # Debug: show uploaded data

            user = request.user
            print(f"User Code: {user.user_code}")  # Debug: user UUID

            for _, row in df.iterrows():
                try:
                    date = pd.to_datetime(row['Date']).date()
                except Exception as e:
                    print(f"Error parsing date: {e}")
                    continue

                route = row['Route']
                try:
                    time = datetime.strptime(row['Time'], "%I:%M %p").strftime("%H:%M")
                except ValueError as e:
                    print(f"Error parsing time: {e}")
                    continue

                num_commuters = row['Commuters']

                print(f"Saving Dataset - Date: {date}, Route: {route}, Time: {time}, Commuters: {num_commuters}, User Code: {user.user_code}")

                Dataset.objects.create(
                    date=date,
                    route=route,
                    time=time,
                    num_commuters=num_commuters,
                    user_code=user.user_code,  # now storing UUID
                    filename=dataset_file.name,
                )

            return redirect('dataset_upload_list')

    # GET request: Fetch datasets
    datasets = Dataset.objects.all()

    # Map user UUIDs to user objects
    user_map = {
        u.user_code: u for u in User.objects.filter(user_code__in=[d.user_code for d in datasets])
    }

    # Attach uploader info to each dataset entry
    for d in datasets:
        d.uploader = user_map.get(d.user_code)

    return render(request, 'admin/datasetUpload.html', {'datasets': datasets})




#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

# views.py

# from django.contrib.auth import get_user_model
# from .models import TemporalEvent

# User = get_user_model()

# def event_list(request):
#     # Get all the events
#     events = TemporalEvent.objects.all()

#     # Pre-fetch users for created_by and updated_by (correct field names)
#     created_by_users = {user.user_code: user for user in User.objects.filter(user_code__in=[event.created_by for event in events])}
#     updated_by_users = {user.user_code: user for user in User.objects.filter(user_code__in=[event.updated_by for event in events if event.updated_by])}

#     # Add the user objects to each event
#     for event in events:
#         event.created_by_user = created_by_users.get(event.created_by)
#         event.updated_by_user = updated_by_users.get(event.updated_by)

#     return render(request, 'admin/datasetTemporal.html', {'events': events})




#-------------------------------------------------------------------------
# !!!don't delete this works in general
# from django.shortcuts import render
# from .models import TemporalEvent

# def event_list(request):
#     events = TemporalEvent.objects.all()
#     return render(request, 'admin/datasetTemporal.html', {'events': events})

#-------------------------------------------------------------------------
from django.shortcuts import render
from .models import TemporalEvent
from django.contrib.auth import get_user_model

User = get_user_model()

def event_list(request):
    events = TemporalEvent.objects.all()

    # Fetch users once to reduce database queries
    user_map = {user.user_code: user for user in User.objects.all()}

    for event in events:
        # Attach the user object for created_by and updated_by
        event.created_by_user = user_map.get(event.created_by)
        event.updated_by_user = user_map.get(event.updated_by)

    return render(request, 'admin/datasetTemporal.html', {'events': events})


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
#fixedEvent

#-------------------------------------------------------------------------

#-------------------------------------------------------------------------


#-------------------------------------------------------------------------

#-------------------------------------------------------------------------


#-------------------------------------------------------------------------

#-------------------------------------------------------------------------


#-------------------------------------------------------------------------
