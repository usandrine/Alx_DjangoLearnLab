from django.urls import path
from . import views

urlpatterns = [
    # Existing URLs...
    
    # Task 2: Security example URLs
    path('example-form/', views.example_form_view, name='example_form'),
    path('secure-search/', views.secure_search_view, name='secure_search'),
    path('xss-safe/', views.xss_safe_view, name='xss_safe'),
    path('secure-books/', views.secure_book_list, name='secure_book_list'),
    path('secure-api/', views.secure_api_view, name='secure_api'),
    path('security-headers/', views.security_headers_view, name='security_headers'),
    
    # Class-based secure views
    path('secure-books-cbv/', views.SecureBookListView.as_view(), name='secure_book_list_cbv'),
    path('secure-books/create/', views.SecureBookCreateView.as_view(), name='secure_book_create'),
]