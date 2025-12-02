"""
Views for bookshelf app with permission-based access control.
Task 1: Implementing permissions in views.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Book, Author, UserProfile

# ============ FUNCTION-BASED VIEWS WITH PERMISSION DECORATORS ============

@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list_view(request):
    """View all books - requires can_view_book permission"""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def book_create_view(request):
    """Create a new book - requires can_create_book permission"""
    if request.method == 'POST':
        # Handle form submission
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        
        if title and author_id and publication_year:
            author = Author.objects.get(id=author_id)
            book = Book.objects.create(
                title=title,
                author=author,
                publication_year=publication_year
            )
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('book_list')
    
    authors = Author.objects.all()
    return render(request, 'bookshelf/book_form.html', {'authors': authors})

@login_required
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def book_edit_view(request, pk):
    """Edit a book - requires can_edit_book permission"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.title = request.POST.get('title', book.title)
        book.publication_year = request.POST.get('publication_year', book.publication_year)
        book.save()
        messages.success(request, f'Book "{book.title}" updated successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_form.html', {'book': book})

@login_required
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def book_delete_view(request, pk):
    """Delete a book - requires can_delete_book permission"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# ============ CLASS-BASED VIEWS WITH PERMISSION MIXINS ============

class BookListView(PermissionRequiredMixin, ListView):
    """List all books - requires can_view_book permission"""
    model = Book
    template_name = 'bookshelf/book_list.html'
    context_object_name = 'books'
    permission_required = 'bookshelf.can_view_book'
    raise_exception = True

class BookDetailView(PermissionRequiredMixin, DetailView):
    """View book details - requires can_view_book permission"""
    model = Book
    template_name = 'bookshelf/book_detail.html'
    permission_required = 'bookshelf.can_view_book'
    raise_exception = True

class BookCreateView(PermissionRequiredMixin, CreateView):
    """Create new book - requires can_create_book permission"""
    model = Book
    template_name = 'bookshelf/book_form.html'
    fields = ['title', 'author', 'publication_year', 'isbn', 'description']
    success_url = reverse_lazy('book_list')
    permission_required = 'bookshelf.can_create_book'
    raise_exception = True

class BookUpdateView(PermissionRequiredMixin, UpdateView):
    """Update book - requires can_edit_book permission"""
    model = Book
    template_name = 'bookshelf/book_form.html'
    fields = ['title', 'author', 'publication_year', 'isbn', 'description']
    success_url = reverse_lazy('book_list')
    permission_required = 'bookshelf.can_edit_book'
    raise_exception = True

class BookDeleteView(PermissionRequiredMixin, DeleteView):
    """Delete book - requires can_delete_book permission"""
    model = Book
    template_name = 'bookshelf/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')
    permission_required = 'bookshelf.can_delete_book'
    raise_exception = True

# ============ AUTHOR VIEWS WITH PERMISSIONS ============

@login_required
@permission_required('bookshelf.can_view_author', raise_exception=True)
def author_list_view(request):
    """List all authors"""
    authors = Author.objects.all()
    return render(request, 'bookshelf/author_list.html', {'authors': authors})

@login_required
@permission_required('bookshelf.can_create_author', raise_exception=True)
def author_create_view(request):
    """Create new author"""
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Author.objects.create(name=name)
            messages.success(request, f'Author "{name}" created successfully!')
            return redirect('author_list')
    return render(request, 'bookshelf/author_form.html')

# ============ CUSTOM PERMISSION CHECK FUNCTIONS ============

def is_editor(user):
    """Check if user is in Editors group"""
    return user.groups.filter(name='Editors').exists()

def is_viewer(user):
    """Check if user is in Viewers group"""
    return user.groups.filter(name='Viewers').exists()

def is_admin_group(user):
    """Check if user is in Admins group"""
    return user.groups.filter(name='Admins').exists()

# ============ GROUP-BASED VIEWS ============

@login_required
@user_passes_test(is_editor)
def editor_dashboard(request):
    """View accessible only to Editors group"""
    return render(request, 'bookshelf/editor_dashboard.html', {
        'message': 'Welcome to Editor Dashboard',
        'user': request.user
    })

@login_required
@user_passes_test(is_viewer)
def viewer_dashboard(request):
    """View accessible only to Viewers group"""
    return render(request, 'bookshelf/viewer_dashboard.html', {
        'message': 'Welcome to Viewer Dashboard',
        'user': request.user
    })

@login_required
@user_passes_test(is_admin_group)
def admin_dashboard(request):
    """View accessible only to Admins group"""
    return render(request, 'bookshelf/admin_dashboard.html', {
        'message': 'Welcome to Admin Dashboard',
        'user': request.user
    })