from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    """Custom User Model"""
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followed_by',
        blank=True
    )
    
    def follow(self, user):
        """Follow another user"""
        if user != self:
            self.following.add(user)
            user.followers.add(self)
            
    def unfollow(self, user):
        """Unfollow another user"""
        if user != self:
            self.following.remove(user)
            user.followers.remove(self)
    
    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-date_joined']