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
    
    path('admin/datasetUpload/', views.dataset_upload_list, name='dataset_upload_list'),



    # path('admin/datasetTemporal/', views.dataset_temporal_list, name='dataset_temporal_list'),
    path('admin/datasetTemporal/', views.event_list, name='event_list'),  # Event list
    path('admin/datasetTemporal/addEvent/', views.add_event, name='add_event'),  # Add event
    path('admin/datasetTemporal/', views.event_list, name='event_list'),  # Event list


    # path('admin/datasetPredictions/', views.datasetprediction_list, name='datasetprediction_list'),
    # path('admin/datasetPredictions/predictCommuters', views.predict_commuters, name='predict_commuters'),

    path('admin/datasetPrediction/', views.predict_commuters, name='datasetprediction_list'),
    path('admin/datasetPrediction/predictCommuters', views.predict_commuters, name='predict_commuters'),




    





    
    



    



    
]
