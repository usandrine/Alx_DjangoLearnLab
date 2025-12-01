from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import CustomUser

def register_view(request):
    """View for registering new users with custom fields"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('custom_users:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'custom_users/register.html', {'form': form})

@login_required
def profile_view(request):
    """View for user profile"""
    return render(request, 'custom_users/profile.html', {'user': request.user})