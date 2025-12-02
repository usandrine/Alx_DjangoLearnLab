from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router (optional)
router = DefaultRouter()

urlpatterns = [
    # ============ BOOK CRUD ENDPOINTS WITH EXACT PATHS ============
    
    # List all books (GET)
    path('books/', views.BookListView.as_view(), name='book-list'),
    
    # Create new book (POST) - authenticated only
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    
    # Get single book details (GET)
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # Update book (PUT/PATCH) - authenticated only
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    
    # Delete book (DELETE) - authenticated only
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # ============ AUTHOR CRUD ENDPOINTS ============
    
    # List all authors (GET)
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    
    # Create new author (POST) - authenticated only
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    
    # Get single author details (GET)
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    
    # Update author (PUT/PATCH) - authenticated only
    path('authors/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    
    # Delete author (DELETE) - authenticated only
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
    
    # ============ COMBINED VIEWS (Alternative) ============
    
    path('books-combined/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books-combined/<int:pk>/', views.BookRetrieveUpdateDestroyView.as_view(), name='book-detail-update-delete'),
    
    # ============ CUSTOM ENDPOINTS ============
    
    path('statistics/', views.BookStatisticsView.as_view(), name='book-statistics'),
    
    # ============ AUTHENTICATION ============
    
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# Optional router URLs
# urlpatterns += router.urls