from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router
router = DefaultRouter()

urlpatterns = [
    # ============ TASK 1: SPECIFIC URL PATTERNS ============
    
    # Book CRUD endpoints (separate views as required)
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Author CRUD endpoints
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
    
    # Combined views (alternative)
    path('books-combined/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books-combined/<int:pk>/', views.BookRetrieveUpdateDestroyView.as_view(), name='book-detail-update-delete'),
    
    # Custom endpoints
    path('statistics/', views.BookStatisticsView.as_view(), name='book-statistics'),
    
    # Authentication
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# Optional: Include router URLs
# urlpatterns += router.urls