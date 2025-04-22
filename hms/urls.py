from django.urls import path
from .views import *

urlpatterns = [
    # path('landing/', hms_landing, name='hms_landing'),

    #user
    path('user/dashboard/', hms_user_dashboard, name='hms_user_dashboard'),
    path('user/faq/', hms_user_faq, name='hms_user_faq'),
    path('user/feedback/', hms_user_feedback, name='hms_user_feedback'),
    
    # agent
    path('agent/dashboard/', hms_agent_dashboard, name='hms_agent_dashboard'),
    path('agent/ticketmgt/', hms_agent_ticketmgt, name='hms_agent_ticketmgt'),

    # support
    path('supp/dashboard/', hms_supp_dashboard, name='hms_supp_dashboard'),
    path('supp/ticketmgt/', hms_supp_ticketmgt, name='hms_supp_ticketmgt'),
    path('supp/usermgt/', hms_supp_usermgt, name='hms_supp_usermgt'),

    # management
    path('mgt/dashboard/', hms_mgt_dashboard, name='hms_mgt_dashboard'),
    path('mgt/auditlog/', hms_mgt_auditlog, name='hms_mgt_auditlog'),
    path('mgt/feedback/', hms_mgt_feedback, name='hms_mgt_feedback'),
    
]