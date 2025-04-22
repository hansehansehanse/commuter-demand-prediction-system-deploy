from django.urls import path
from .views import *
from . import views



urlpatterns = [

    path('admin/dashboard', cdps_admin_dashboard, name='cdps_admin_dashboard'),
    path('admin/dashboard2', cdps_admin_dashboard2, name='cdps_admin_dashboard2'),
    
    
    path('admin/accountManagement/', views.user_list, name='account_management'),
    path('admin/accountManagement/add-user/', views.add_user, name='add_user'),

    # path('add-user/', views.add_user, name='add_user'),

    # path('users/', views.user_list, name='user_list'),
   
    
]
