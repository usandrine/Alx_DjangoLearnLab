from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
import os

# Custom User Manager
class CustomUserManager(BaseUserManager):
    """Custom manager for CustomUser model"""
    
    def create_user(self, email, username, date_of_birth, password=None, **extra_fields):
        """
        Create and save a regular user with given email, username, date_of_birth and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_('The Username must be set'))
        if not date_of_birth:
            raise ValueError(_('The Date of Birth must be set'))
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            date_of_birth=date_of_birth,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, date_of_birth, password=None, **extra_fields):
        """
        Create and save a SuperUser with given email, username, date_of_birth and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, username, date_of_birth, password, **extra_fields)

# Function for profile photo upload path
def user_profile_photo_path(instance, filename):
    """Generate path for user profile photos"""
    ext = filename.split('.')[-1]
    filename = f'profile_photo_{instance.id}.{ext}'
    return os.path.join('profile_photos', filename)

# Custom User Model
class CustomUser(AbstractUser):
    """
    Custom user model with additional fields.
    This model extends Django's AbstractUser.
    """
    
    # Additional fields
    date_of_birth = models.DateField(
        _('date of birth'),
        null=True,
        blank=False,
        help_text=_('Required. Format: YYYY-MM-DD')
    )
    
    profile_photo = models.ImageField(
        _('profile photo'),
        upload_to=user_profile_photo_path,
        null=True,
        blank=True,
        help_text=_('Upload a profile photo')
    )
    
    # Use email as the unique identifier instead of username
    email = models.EmailField(_('email address'), unique=True)
    
    # Custom fields
    bio = models.TextField(_('biography'), max_length=500, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=15, blank=True)
    
    # Set email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'date_of_birth']
    
    # Use custom manager
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the full name of the user"""
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']

# Update existing models to use CustomUser
from django.conf import settings

class UserProfile(models.Model):
    """Extended user profile with role-based permissions"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('librarian', 'Librarian'),
        ('member', 'Member'),
    ]
    
    # Use settings.AUTH_USER_MODEL to reference the custom user model
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # This is the key change
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    
    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
    
    def __str__(self):
        return f"{self.user.email} - {self.get_role_display()}"