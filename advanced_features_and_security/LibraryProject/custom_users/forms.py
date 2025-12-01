from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users with custom fields"""
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'date_of_birth', 'profile_photo')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make date_of_birth required in form
        self.fields['date_of_birth'].required = True


class CustomUserChangeForm(UserChangeForm):
    """Form for updating existing users"""
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'date_of_birth', 'profile_photo', 'bio', 'phone_number')