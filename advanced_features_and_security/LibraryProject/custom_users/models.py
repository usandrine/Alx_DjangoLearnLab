from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
import os

class CustomUserManager(BaseUserManager):
    """Custom manager for CustomUser model"""
    
    def create_user(self, email, username, date_of_birth, password=None, **extra_fields):
        """
        Create and save a regular user with the given email, username, date of birth and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_('The Username must be set'))
        
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
        Create and save a SuperUser with the given email, username, date of birth and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, username, date_of_birth, password, **extra_fields)


def user_profile_photo_path(instance, filename):
    """Generate path for user profile photos"""
    ext = filename.split('.')[-1]
    filename = f'profile_photo_{instance.id}.{ext}'
    return os.path.join('profile_photos', filename)


class CustomUser(AbstractUser):
    """Custom user model with additional fields"""
    
    email = models.EmailField(_('email address'), unique=True)
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    profile_photo = models.ImageField(
        _('profile photo'),
        upload_to=user_profile_photo_path,
        null=True,
        blank=True
    )
    
    # Custom fields can be added here
    bio = models.TextField(_('biography'), max_length=500, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=15, blank=True)
    
    # Use email as the unique identifier instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'date_of_birth']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')