from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API endpoints - ADD THIS LINE EXPLICITLY
    path('api/', include('api.urls')),
    
    # Alternative: also include at root for testing
    path('', include('api.urls')),
]

# OR Try this alternative format:
"""
from django.contrib import admin
from django.urls import path, include

# Main URL configuration for advanced-api-project
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include API URLs - MAKE SURE THIS LINE EXISTS
    path('', include('api.urls')),
    
    # Also include with api/ prefix
    path('api/', include('api.urls')),
]
"""