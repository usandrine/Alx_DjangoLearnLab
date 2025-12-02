"""
Management command to setup user groups with permissions.
Run: python manage.py setup_groups
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book, Author, UserProfile

class Command(BaseCommand):
    help = 'Setup user groups and assign permissions'
    
    def handle(self, *args, **kwargs):
        # Get content types
        book_content_type = ContentType.objects.get_for_model(Book)
        author_content_type = ContentType.objects.get_for_model(Author)
        profile_content_type = ContentType.objects.get_for_model(UserProfile)
        
        # Get all permissions
        book_permissions = Permission.objects.filter(content_type=book_content_type)
        author_permissions = Permission.objects.filter(content_type=author_content_type)
        profile_permissions = Permission.objects.filter(content_type=profile_content_type)
        
        # Create Groups
        admins_group, created = Group.objects.get_or_create(name='Admins')
        editors_group, created = Group.objects.get_or_create(name='Editors')
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        
        # Assign permissions to Admins group (all permissions)
        all_permissions = list(book_permissions) + list(author_permissions) + list(profile_permissions)
        admins_group.permissions.set(all_permissions)
        self.stdout.write(self.style.SUCCESS(f'Assigned all permissions to Admins group'))
        
        # Assign permissions to Editors group (create and edit)
        editor_perms = []
        editor_perms.extend(book_permissions.filter(codename__in=['can_view_book', 'can_create_book', 'can_edit_book']))
        editor_perms.extend(author_permissions.filter(codename__in=['can_view_author', 'can_create_author', 'can_edit_author']))
        editor_perms.extend(profile_permissions.filter(codename='can_view_profile'))
        
        editors_group.permissions.set(editor_perms)
        self.stdout.write(self.style.SUCCESS(f'Assigned editor permissions to Editors group'))
        
        # Assign permissions to Viewers group (view only)
        viewer_perms = []
        viewer_perms.extend(book_permissions.filter(codename='can_view_book'))
        viewer_perms.extend(author_permissions.filter(codename='can_view_author'))
        viewer_perms.extend(profile_permissions.filter(codename='can_view_profile'))
        
        viewers_group.permissions.set(viewer_perms)
        self.stdout.write(self.style.SUCCESS(f'Assigned viewer permissions to Viewers group'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\nGroups created and permissions assigned:'))
        self.stdout.write(f'  - Admins: {admins_group.permissions.count()} permissions')
        self.stdout.write(f'  - Editors: {editors_group.permissions.count()} permissions')
        self.stdout.write(f'  - Viewers: {viewers_group.permissions.count()} permissions')