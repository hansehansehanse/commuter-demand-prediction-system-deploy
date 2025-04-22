from django.shortcuts import render

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
from django.shortcuts import render
from .models import CustomUser

def user_list(request):
    print("✅ user_list being called")
    users = CustomUser.objects.all()
    print(f"🧾 Users in DB: {users}")
    return render(request, 'admin/accountManagement.html', {'users': users})



# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import CustomUser
# from django.contrib.auth.hashers import make_password

# def user_list(request):
#     users = CustomUser.objects.all()
#     return render(request, 'admin/accountManagement.html', {'users': users})

#-------------------------------------------------------------------------
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def add_user(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         phone_number = request.POST.get('phone_number')
#         access_level = request.POST.get('access_level')
#         verified = request.POST.get('verified')
#         password = request.POST.get('password')

#         user = CustomUser(
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             phone_number=phone_number,
#             access_level=access_level,
#             verified=verified,
#             password=make_password(password),  # Hash the password before saving
#         )
#         user.save()

#         return JsonResponse({'message': 'User successfully added!'}, status=200)
#     return JsonResponse({'error': 'Invalid request method.'}, status=400)


#-------------------------------------------------------------------------
from django.shortcuts import render
from django.http import JsonResponse
from .models import CustomUser
from django.contrib.auth.hashers import make_password  # To hash password before saving

import json
import uuid


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
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


#-------------------------------------------------------------------------

#-------------------------------------------------------------------------

#-------------------------------------------------------------------------

#-------------------------------------------------------------------------

#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
