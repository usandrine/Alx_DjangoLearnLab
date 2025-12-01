from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book, Author, Library, UserProfile

class Command(BaseCommand):
    help = 'Setup user groups and permissions'
    
    def handle(self, *args, **kwargs):
        # Get content types
        book_content_type = ContentType.objects.get_for_model(Book)
        author_content_type = ContentType.objects.get_for_model(Author)
        library_content_type = ContentType.objects.get_for_model(Library)
        profile_content_type = ContentType.objects.get_for_model(UserProfile)
        
        # Get all permissions
        book_permissions = Permission.objects.filter(content_type=book_content_type)
        author_permissions = Permission.objects.filter(content_type=author_content_type)
        library_permissions = Permission.objects.filter(content_type=library_content_type)
        profile_permissions = Permission.objects.filter(content_type=profile_content_type)
        
        # Create Groups
        admin_group, created = Group.objects.get_or_create(name='Admins')
        editor_group, created = Group.objects.get_or_create(name='Editors')
        viewer_group, created = Group.objects.get_or_create(name='Viewers')
        member_group, created = Group.objects.get_or_create(name='Members')
        
        # Assign permissions to Admins (all permissions)
        admin_group.permissions.set(
            list(book_permissions) + 
            list(author_permissions) + 
            list(library_permissions) + 
            list(profile_permissions)
        )
        
        # Assign permissions to Editors (create, edit, view)
        editor_group.permissions.set(
            list(book_permissions.filter(codename__in=['can_view_book', 'can_create_book', 'can_edit_book'])) +
            list(author_permissions.filter(codename__in=['can_view_author', 'can_create_author', 'can_edit_author'])) +
            list(library_permissions.filter(codename__in=['can_view_library', 'can_create_library', 'can_edit_library'])) +
            list(profile_permissions.filter(codename__in=['can_view_profile']))
        )
        
        # Assign permissions to Viewers (view only)
        viewer_group.permissions.set(
            list(book_permissions.filter(codename='can_view_book')) +
            list(author_permissions.filter(codename='can_view_author')) +
            list(library_permissions.filter(codename='can_view_library')) +
            list(profile_permissions.filter(codename='can_view_profile'))
        )
        
        # Assign permissions to Members (view only + some extras)
        member_group.permissions.set(
            list(book_permissions.filter(codename='can_view_book')) +
            list(author_permissions.filter(codename='can_view_author')) +
            list(library_permissions.filter(codename='can_view_library')) +
            list(profile_permissions.filter(codename__in=['can_view_profile', 'can_edit_profile']))
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully created groups and assigned permissions'))