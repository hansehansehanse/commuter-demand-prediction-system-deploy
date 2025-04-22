from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cdps/', include('CommuterDemandPredictionSystem.urls')),
    path('hms/', include('hms.urls')),
]

