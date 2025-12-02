"""
Main URL configuration for advanced-api-project
MAKE SURE THIS FILE INCLUDES THE API URLS
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # THIS IS THE CRITICAL LINE - Include API URLs
    path('api/', include('api.urls')),
    
    # Optional: Also include at root
    path('', include('api.urls')),
]