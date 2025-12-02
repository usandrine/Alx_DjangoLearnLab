from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """Form for creating new CustomUser"""
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'date_of_birth')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].required = True

class CustomUserChangeForm(UserChangeForm):
    """Form for updating existing CustomUser"""
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'date_of_birth', 'profile_photo', 'bio', 'phone_number')