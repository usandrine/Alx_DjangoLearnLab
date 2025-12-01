# relationship_app/management/commands/assign_roles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from relationship_app.models import UserProfile

class Command(BaseCommand):
    help = 'Assign roles to existing users'
    
    def handle(self, *args, **kwargs):
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@library.com', 'is_staff': True}
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
        
        # Assign admin role
        profile, _ = UserProfile.objects.get_or_create(user=admin_user)
        profile.role = 'admin'
        profile.save()
        
        self.stdout.write(self.style.SUCCESS(f'Assigned admin role to {admin_user.username}'))
        
        # You can add more users here
        self.stdout.write(self.style.SUCCESS('Role assignment completed'))