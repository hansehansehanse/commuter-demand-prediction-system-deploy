from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='login/', permanent=False)),  
    path('/cdps', RedirectView.as_view(url='login/', permanent=False)),

    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/cdps/login/'), name='logout'),
    path('signup/', views.signup_view, name='signup'),

    path('admin/profile/', profile_view, name='profile_view'),
    path('busManager/profile/', profile_view2, name='profile_view2'),
    

    path('admin/dashboard/', views.dashboard, name='dashboard'),
    path('busManager/dashboard/', views.dashboard2, name='dashboard2'),

    path("admin/dashboard/monthlyCommuterStats/", views.monthly_commuter_stats, name="monthly_commuter_stats"),
    path("admin/dashboard/commutersPerRoute/", views.route_commuter_percentages, name="route_commuter_percentages"),
    path('admin/dashboard/topTimes/', views.top_commuter_times, name='top_commuter_times'),
    path('admin/dashboard/heatmap/', views.commuters_heatmap_data, name='commuters_heatmap_data'),
    path('admin/dashboard/dailyCommuterTrend/', views.daily_commuter_trend, name='daily_commuter_trend'),
    path('admin/dashboard/dailyCommuterTrendPerRoute/', views.daily_commuter_trend_per_route, name='daily_commuter_trend_per_route'),
    path('admin/dashboard/dailyCommuterTrendPerTime/', views.daily_commuter_trend_per_time, name='daily_commuter_trend_per_time'),

    path('admin/dashboard/modelLatestInfo/', views.get_latest_model_info, name='latest_model_info'),

    path('admin/dashboard/upcomingEvents/', views.upcoming_events_view, name='upcoming_events'),




      
    path('admin/accountManagement/', views.user_list, name='account_management'),
    path('admin/accountManagement/add-user/', views.add_user, name='add_user'),
    path('admin/accountManagement/edit-user/', views.edit_user, name='edit_user'),
    path('admin/accountManagement/delete-user/', views.delete_user, name='delete_user'),


    path('admin/actionLog/', views.action_log_list, name='action_log_list'), 
    path('admin/actionLog/exportActionLog', views.action_log_export, name='action_log_export'),

    

    path('admin/datasetTemporal/', views.event_list, name='event_list'),  # Event list
    path('admin/datasetTemporal/addEvent/', views.add_event, name='add_event'),  # Add event
    


    path('admin/datasetTemporal/edit-event/', views.edit_event, name='edit_event'),
    path('admin/datasetTemporal/delete-event/', views.delete_event, name='delete_event'),

   
    path('admin/datasetGraph/', views.dataset_graph, name='dataset_graph'),
    path('busManager/datasetGraph/', views.dataset_graph2, name='dataset_graph2'),

    path('admin/historicalDatasetUpload/upload', views.historical_dataset_upload_list, name='historical_dataset_upload_list'),
    path('admin/historicalDatasetUpload/delete', views.delete_all_historical_datasets, name='delete_historical_datasets'),
    path('admin/historicalDatasetUpload/dataset', views.historical_dataset_event_list, name='historical_dataset_event_list'),

    path('admin/historicalDatasetUpload/admin/historicalDatasetUpload/export', views.historical_dataset_export, name='historical_dataset_export'),

    path('admin/historicalDatasetUpload/admin/train-model/', views.train_random_forest_model_view, name='train_random_forest_model'),

    path('admin/historicalDatasetUpload/addSingle/', views.add_single_historical_data, name='add_single_historical_data'),


    path('admin/historicalDatasetUpload/addHistoricalEvent/', views.add_historical_event, name='add_historical_event'),
    path('admin/historicalDatasetUpload/editHistoricalEvent/', views.edit_historical_event, name='edit_historical_event'),
    path('admin/historicalDatasetUpload/deleteHistoricalEvent/', views.delete_historical_event, name='delete_historical_event'),


    
   



    



    
    
    




    




    





    
    



    



    
]
