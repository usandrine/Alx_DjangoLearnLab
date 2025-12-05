from django.contrib import admin
from django.urls import path, include

from api_project.api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('search/', views.search_view, name='search'),
    path('tags/<slug:tag_slug>/', views.tag_view, name='tag_posts'),
]