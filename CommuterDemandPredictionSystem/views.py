from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import make_password

from .models import CustomUser

import json
import uuid

import logging

emp_sidebar_items = [
    {'url':'hris_emp_dashboard', 'icon_class':'ti-smart-home', 'name':'Dashboard'},
    {'url':'hris_emp_records', 'icon_class':'ti-file', 'name':'Records'},
    {'url':'hris_emp_payroll', 'icon_class':'ti-file-dollar', 'name':'Payroll'},
    {'url':'hris_emp_leaves', 'icon_class':'ti-checkbox', 'name':'Leaves'},
]
# Create your views here.

#-------------------------------------------------------------------------
def cdps_admin_dashboard(request):
    # context = {'sidebar_items':emp_sidebar_items}
    context = {}
    return render(request, 'admin/dashboard.html', context)

def cdps_admin_dashboard2(request):
    # context = {'sidebar_items':emp_sidebar_items}
    context = {}
    return render(request, 'admin/dashboard2.html', context)

#-------------------------------------------------------------------------
#admin
def cdps_admin_accountManagement(request):
    # context = {'sidebar_items':emp_sidebar_items}
    context = {}
    return render(request, 'admin/accountManagement.html', context)


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
# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import CustomUser
# from django.contrib.auth.hashers import make_password  # To hash password before saving

# import json
# import uuid

logger = logging.getLogger(__name__)

def add_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("📩 Received data:", data)  # ADD THIS TO DEBUG

            user = CustomUser.objects.create_user(
                username=str(uuid.uuid4()),
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', ''),
                email=data.get('email', ''),
                phone_number=data.get('phone_number', ''),
                access_level=data.get('access_level', 'Bus Manager'),
                verified=data.get('verified', False),
                password=data.get('password', 'temporary123'),
            )

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
        user.delete()
        return JsonResponse({"message": "User deleted successfully."})
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

#-------------------------------------------------------------------------

#-------------------------------------------------------------------------

#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
