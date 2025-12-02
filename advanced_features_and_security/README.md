# Django Permissions and Groups Setup Guide

## Overview
This project implements a comprehensive permission and group system for managing access control in a Django application.

## Custom Permissions

### Book Model Permissions
The `Book` model has the following custom permissions:
- `can_view_book` - View books
- `can_create_book` - Create new books
- `can_edit_book` - Edit existing books
- `can_delete_book` - Delete books

### Author Model Permissions
The `Author` model has similar permissions:
- `can_view_author`
- `can_create_author`
- `can_edit_author`
- `can_delete_author`

## User Groups

Three user groups are configured:

### 1. Admins Group
- **Permissions**: All permissions (view, create, edit, delete)
- **Access**: Full system access
- **Setup Command**: `python manage.py setup_groups`

### 2. Editors Group
- **Permissions**: View, create, and edit permissions
- **Access**: Can view, create, and edit content but cannot delete
- **Setup Command**: `python manage.py setup_groups`

### 3. Viewers Group
- **Permissions**: View-only permissions
- **Access**: Can only view content, cannot modify
- **Setup Command**: `python manage.py setup_groups`

## View Protection

### Function-Based Views
Views are protected using Django's permission decorators:

```python
@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def book_create_view(request):
    # Only users with can_create_book permission can access
    pass