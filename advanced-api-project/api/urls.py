from django.urls import path, include
from . import views

urlpatterns = [
    # ============ BOOK CRUD ENDPOINTS ============
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # ============ AUTHOR CRUD ENDPOINTS ============
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
    
    # ============ COMBINED VIEWS ============
    path('books-combined/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books-combined/<int:pk>/', views.BookRetrieveUpdateDestroyView.as_view(), name='book-detail-update-delete'),
    
    # ============ CUSTOM VIEWS ============
    path('statistics/', views.BookStatisticsView.as_view(), name='book-statistics'),
    path('librarian/', views.LibrarianOnlyView.as_view(), name='librarian-view'),
    
    # ============ AUTHENTICATION ============
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]