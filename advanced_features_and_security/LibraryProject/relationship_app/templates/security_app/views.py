from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.db import connection
from django.utils.html import escape

@csrf_protect
def secure_form_view(request):
    """Example of secure form handling"""
    if request.method == 'POST':
        # Safe input handling - using Django forms would be better
        user_input = escape(request.POST.get('search', ''))
        
        # Safe SQL query (using Django ORM)
        from relationship_app.models import Book
        books = Book.objects.filter(title__icontains=user_input)
        
        # NEVER DO THIS: Unsafe SQL
        # unsafe_query = f"SELECT * FROM relationship_app_book WHERE title LIKE '%{user_input}%'"
        # with connection.cursor() as cursor:
        #     cursor.execute(unsafe_query)  # Vulnerable to SQL injection!
        
        return render(request, 'security_app/results.html', {'books': books})
    
    return render(request, 'security_app/search_form.html')

def xss_safe_view(request):
    """Example of XSS-safe template rendering"""
    # User input that will be automatically escaped in templates
    user_data = {
        'username': request.GET.get('name', 'Guest'),
        'bio': request.GET.get('bio', 'No bio provided'),
    }
    return render(request, 'security_app/profile.html', user_data)