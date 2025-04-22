# hms/views.py
from django.shortcuts import render
#user
user_sidebar_items = [
    {'url': 'hms_user_dashboard', 'icon_class': 'ti-smart-home', 'name': 'Dashboard'},
    {'url': 'hms_user_faq', 'icon_class': 'ti-messages', 'name': 'FAQ'},
    {'url': 'hms_user_feedback', 'icon_class': 'ti-stars', 'name': 'Feedback'},
]

#agent
agent_sidebar_items = [
     {'url': 'hms_agent_dashboard', 'icon_class': 'ti-smart-home', 'name': 'Dashboard'},
     {'url': 'hms_agent_ticketmgt', 'icon_class': 'ti-ticket', 'name': 'Ticket Management'},
]


#support
supp_sidebar_items = [
    {'url': 'hms_supp_dashboard', 'icon_class': 'ti-smart-home', 'name': 'Dashboard'},
    {'url': 'hms_supp_ticketmgt', 'icon_class': 'ti-ticket', 'name': 'Ticket Management'},
    {'url': 'hms_supp_usermgt', 'icon_class': 'ti-users', 'name': 'User Management'},
]
#management
mgt_sidebar_items = [ 
    {'url': 'hms_mgt_dashboard', 'icon_class': 'ti-smart-home', 'name': 'Dashboard'},
    {'url': 'hms_mgt_auditlog', 'icon_class': 'ti-book', 'name': 'Audit Logs'},
    {'url': 'hms_mgt_feedback', 'icon_class': 'ti-stars', 'name': 'Feedback Overview'},
]

#-----------------------------------------------------------------------------------------------#

def hms_landing(request):
    context = {}
    return render(request, 'hms/hms_landing.html', context)

#user
def hms_user_dashboard(request):
    context = {'sidebar_items': user_sidebar_items}
    return render(request, 'hms/user_dashboard.html', context)

def hms_user_faq(request):
    context = {'sidebar_items':user_sidebar_items}
    return render(request, 'hms/user_faq.html', context)

def hms_user_feedback(request):
    context = {'sidebar_items':user_sidebar_items}
    return render(request, 'hms/user_feedback.html', context)

#-----------------------------------------------------------------------------------------------#
#agent
def hms_agent_dashboard(request):
    context = {'sidebar_items': agent_sidebar_items}
    return render(request, 'hms/agent_dashboard.html', context)

def hms_agent_ticketmgt(request):
    context = {'sidebar_items': agent_sidebar_items}
    return render(request, 'hms/agent_ticketmgt.html', context)

#-----------------------------------------------------------------------------------------------#
#support
def hms_supp_dashboard(request):
    context = {'sidebar_items': supp_sidebar_items}
    return render(request, 'hms/supp_dashboard.html', context)

def hms_supp_ticketmgt(request):
    context = {'sidebar_items': supp_sidebar_items}
    return render(request, 'hms/supp_ticketmgt.html', context)

def hms_supp_usermgt(request):
    context = {'sidebar_items': supp_sidebar_items}
    return render(request, 'hms/supp_usermgt.html', context)
#-----------------------------------------------------------------------------------------------#
#management
def hms_mgt_dashboard(request):
    context = {'sidebar_items': mgt_sidebar_items}
    return render(request, 'hms/mgt_dashboard.html', context)

def hms_mgt_auditlog(request):
    context = {'sidebar_items': mgt_sidebar_items}
    return render(request, 'hms/mgt_auditlog.html', context)

def hms_mgt_feedback(request):
    context = {'sidebar_items': mgt_sidebar_items}
    return render(request, 'hms/mgt_feedback.html', context)