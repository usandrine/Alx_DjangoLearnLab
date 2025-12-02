from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
import os
from django.conf import settings

# ... Keep your existing CustomUser and CustomUserManager classes ...

# Book Model with Custom Permissions
class Book(models.Model):
    """
    Book model with custom permissions for CRUD operations.
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='books')
    publication_year = models.IntegerField()
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        # Custom permissions as specified in the task
        permissions = [
            ("can_view_book", "Can view book"),
            ("can_create_book", "Can create book"),
            ("can_edit_book", "Can edit book"),
            ("can_delete_book", "Can delete book"),
        ]
        ordering = ['title']
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"

# Author Model (for foreign key reference)
class Author(models.Model):
    """Author model"""
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    class Meta:
        permissions = [
            ("can_view_author", "Can view author"),
            ("can_create_author", "Can create author"),
            ("can_edit_author", "Can edit author"),
            ("can_delete_author", "Can delete author"),
        ]
    
    def __str__(self):
        return self.name

# UserProfile model (keep existing)
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('librarian', 'Librarian'),
        ('member', 'Member'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    
    class Meta:
        permissions = [
            ("can_view_profile", "Can view profile"),
            ("can_edit_profile", "Can edit profile"),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.get_role_display()}"