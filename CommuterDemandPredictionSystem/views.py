
from django.shortcuts import render
from django.http import JsonResponse
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

            # Print the first few rows to see the format
            print(df.head())

            # Get the user_code from the logged-in user
            user = request.user
            print(f"User Code: {user.user_code}")  # Print user code for debugging

            # Loop through the dataframe and save each row to the model
            for _, row in df.iterrows():
                # Convert the date to the correct format
                try:
                    date = pd.to_datetime(row['Date']).date()  # Extract just the date part
                except Exception as e:
                    print(f"Error parsing date: {e}")
                    continue  # Skip this row if there's a problem with the date

                route = row['Route']
                
                # Convert the time to 24-hour format
                try:
                    time = datetime.strptime(row['Time'], "%I:%M %p").strftime("%H:%M")
                except ValueError as e:
                    print(f"Error parsing time: {e}")
                    continue  # Skip this row if there's a problem with the time

                num_commuters = row['Commuters']

                # Print data before saving it
                print(f"Saving Dataset - Date: {date}, Route: {route}, Time: {time}, Commuters: {num_commuters}, User Code: {user.user_code}")

                Dataset.objects.create(
                    date=date,
                    route=route,
                    time=time,
                    num_commuters=num_commuters,
                    user_code=user,  # user who uploaded
                    filename=dataset_file.name,  # 🆕 Save the filename here
                )


            return redirect('dataset_upload_list')  # Redirect back to the page after uploading

    # Fetch all dataset entries from the database
    datasets = Dataset.objects.all()

    # Pass the datasets to the template
    return render(request, 'admin/datasetUpload.html', {'datasets': datasets})


#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

from django.shortcuts import render
from .models import ImportantEvent, Dataset  # Import your other model

def dataset_temporal_list(request):
    # Fetch both datasets
    events = ImportantEvent.objects.all()  # Fetch events data
    temporal_data = Dataset.objects.all()  # Replace with your actual model for the temporal list
    
    return render(request, 'admin/datasetTemporal.html', {
        'events': events,  # Pass the events dataset
        'temporal_data': temporal_data,  # Pass the other dataset (replace Dataset with your actual model)
    })

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

# from django.shortcuts import render
# from .models import Dataset

# def dataset_temporal_list(request):
#     # Fetch all dataset entries
#     datasets = Dataset.objects.all().order_by('-date')  # Order by date, most recent first
    
#     # Pass datasets to template
#     return render(request, 'admin/datasetTemporal.html', {'datasets': datasets})

from .models import ImportantEvent

def dataset_temporal_list(request):
    # Fetch all events, order by date (most recent first)
    events = ImportantEvent.objects.all().order_by('-date')

    # Pass events to the template
    return render(request, 'admin/datasetTemporal.html', {'datasets': events})  # Use 'datasets' in context


#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

from django.shortcuts import render

from django.http import JsonResponse
from .models import ImportantEvent
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# @csrf_exempt  # If you don't want to manually handle CSRF for now (later you can improve this)
def dataset_addEvent(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event_name = data.get('event_name')
            event_type = data.get('event_type')
            date = data.get('date')
            
            # Save to database (assuming you have an ImportantEvent model)
            ImportantEvent.objects.create(
                event_name=event_name,
                event_type=event_type,
                date=date
            )
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



#-------------------------------------------------------------------------


#-------------------------------------------------------------------------

#-------------------------------------------------------------------------


#-------------------------------------------------------------------------

#-------------------------------------------------------------------------


#-------------------------------------------------------------------------

#-------------------------------------------------------------------------


#-------------------------------------------------------------------------
