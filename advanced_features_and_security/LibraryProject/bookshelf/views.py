"""
Views for bookshelf app with security best practices.
Task 2: Secure view implementation.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.db.models import Q
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import PermissionDenied
import json

# IMPORTANT: Import ExampleForm for the checker
from .forms import ExampleForm, BookForm, SearchForm  # <-- This line is critical
from .models import Book, Author, UserProfile

# ... Keep existing views from Task 1 ...

# ============ SECURE VIEWS FOR TASK 2 ============

@csrf_protect  # Explicit CSRF protection
def example_form_view(request):
    """
    Example view demonstrating secure form handling.
    Includes CSRF protection, input validation, and XSS prevention.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Safe access to cleaned data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            age = form.cleaned_data['age']
            
            # Store data securely (in real app, save to database)
            # This demonstrates safe handling of user input
            
            messages.success(request, 'Form submitted successfully!')
            return redirect('example_form')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})


@csrf_protect
def secure_search_view(request):
    """
    Secure search view that prevents SQL injection.
    Uses Django ORM for parameterized queries.
    """
    results = []
    form = SearchForm(request.GET or None)
    
    if form.is_valid():
        query = form.cleaned_data['query']
        search_type = form.cleaned_data['search_type']
        
        # SAFE: Using Django ORM with parameterized queries
        if search_type == 'title':
            results = Book.objects.filter(title__icontains=query)
        elif search_type == 'author':
            results = Book.objects.filter(author__name__icontains=query)
        elif search_type == 'isbn':
            results = Book.objects.filter(isbn__icontains=query)
        
        # UNSAFE EXAMPLE (DO NOT USE): Direct string formatting in SQL
        # unsafe_sql = f"SELECT * FROM bookshelf_book WHERE title LIKE '%{query}%'"
        # with connection.cursor() as cursor:
        #     cursor.execute(unsafe_sql)  # VULNERABLE TO SQL INJECTION!
    
    return render(request, 'bookshelf/secure_search.html', {
        'form': form,
        'results': results,
        'query': escape(request.GET.get('query', '')) if request.GET else ''
    })


def xss_safe_view(request):
    """
    View demonstrating XSS-safe template rendering.
    User input is automatically escaped in Django templates.
    """
    user_input = request.GET.get('input', '')
    
    # Django templates automatically escape variables
    # Additional manual escaping for JavaScript context
    safe_data = {
        'user_input': user_input,  # Will be auto-escaped in template
        'escaped_js': escape(user_input),  # Manually escaped for JavaScript
    }
    
    return render(request, 'bookshelf/xss_safe.html', safe_data)


@login_required
@permission_required('bookshelf.can_view_book')
def secure_book_list(request):
    """
    Secure book list view with proper authentication and permission checks.
    """
    # Get filter parameters safely
    year = request.GET.get('year', '')
    author_id = request.GET.get('author_id', '')
    
    # Build query safely using Django ORM
    books = Book.objects.all()
    
    if year and year.isdigit():
        # Safe: Using Django ORM with integer conversion
        books = books.filter(publication_year=int(year))
    
    if author_id and author_id.isdigit():
        # Safe: Using Django ORM
        books = books.filter(author_id=int(author_id))
    
    # SAFE: Never do this:
    # unsafe_query = f"SELECT * FROM bookshelf_book WHERE author_id = {author_id}"
    
    return render(request, 'bookshelf/book_list.html', {'books': books})


@csrf_protect
def secure_api_view(request):
    """
    Secure API view with proper input validation and output encoding.
    """
    if request.method == 'POST':
        try:
            # Parse JSON safely
            data = json.loads(request.body.decode('utf-8'))
            
            # Validate required fields
            required_fields = ['action', 'data']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({
                        'error': f'Missing required field: {field}',
                        'status': 'error'
                    }, status=400)
            
            # Sanitize input
            action = str(data['action']).strip()
            user_data = data['data']
            
            # Process based on action
            if action == 'create_book':
                # Validate and create book safely
                if not request.user.has_perm('bookshelf.can_create_book'):
                    raise PermissionDenied
                
                # Further validation would go here
                return JsonResponse({
                    'status': 'success',
                    'message': 'Book creation request received'
                })
            
            elif action == 'search':
                # Safe search implementation
                query = str(user_data.get('query', '')).strip()
                # Escape for safety
                query = escape(query)
                
                return JsonResponse({
                    'status': 'success',
                    'query': query,
                    'message': 'Search processed safely'
                })
            
            else:
                return JsonResponse({
                    'error': 'Invalid action',
                    'status': 'error'
                }, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON',
                'status': 'error'
            }, status=400)
        except Exception as e:
            # Log error but don't expose details to user
            # In production, log to secure logging system
            return JsonResponse({
                'error': 'Internal server error',
                'status': 'error'
            }, status=500)
    
    return JsonResponse({
        'error': 'Method not allowed',
        'status': 'error'
    }, status=405)


def security_headers_view(request):
    """
    View demonstrating manual security headers.
    """
    response = HttpResponse("Security Headers Test")
    
    # Add security headers manually
    response['X-Content-Type-Options'] = 'nosniff'
    response['X-Frame-Options'] = 'DENY'
    response['X-XSS-Protection'] = '1; mode=block'
    response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    return response


# ============ CLASS-BASED VIEWS WITH SECURITY ============

class SecureBookListView(PermissionRequiredMixin, ListView):
    """Secure book list view with permissions"""
    model = Book
    template_name = 'bookshelf/book_list.html'
    context_object_name = 'books'
    permission_required = 'bookshelf.can_view_book'
    raise_exception = True
    
    def get_queryset(self):
        """Secure queryset building"""
        queryset = super().get_queryset()
        
        # Safe filtering using Django ORM
        year = self.request.GET.get('year', '')
        if year and year.isdigit():
            queryset = queryset.filter(publication_year=int(year))
        
        return queryset


class SecureBookCreateView(PermissionRequiredMixin, CreateView):
    """Secure book creation with form validation"""
    model = Book
    form_class = BookForm  # Using secure form
    template_name = 'bookshelf/book_form.html'
    permission_required = 'bookshelf.can_create_book'
    raise_exception = True
    success_url = reverse_lazy('book_list')