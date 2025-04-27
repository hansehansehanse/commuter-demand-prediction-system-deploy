from django.urls import path
from .views import *
from . import views



urlpatterns = [

    path('login/', login_view, name='login'),


    # path('admin/dashboard', cdps_admin_dashboard, name='cdps_admin_dashboard'),
    # path('admin/dashboard2', cdps_admin_dashboard2, name='cdps_admin_dashboard2'),
    
    
    path('admin/accountManagement/', views.user_list, name='account_management'),
    path('admin/accountManagement/add-user/', views.add_user, name='add_user'),
    path('admin/accountManagement/edit-user/', views.edit_user, name='edit_user'),
    path('admin/accountManagement/delete-user/', views.delete_user, name='delete_user'),


    # path('admin/actionLog/', views.cdps_admin_actionLog, name='action_log'),                    # change later
    path('admin/actionLog/', views.action_log_list, name='action_log_list'), 
    
    # path('action-log/', views.action_log_list, name='action_log_list'),

    # other paths...


   
    
]
