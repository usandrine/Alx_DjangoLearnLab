from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'custom_users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='custom_users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='custom_users/logout.html'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
]