from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for API views
router = DefaultRouter()

urlpatterns = [
    # Book endpoints
    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', views.BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
    
    # Author endpoints
    path('authors/', views.AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', views.AuthorRetrieveUpdateDestroyView.as_view(), name='author-detail'),
    
    # Custom endpoints
    path('statistics/', views.BookStatisticsView.as_view(), name='book-statistics'),
    path('authors/<int:author_id>/books/', views.AuthorBooksView.as_view(), name='author-books'),
    
    # API documentation
    path('api-auth/', include('rest_framework.urls')),
]

# For ViewSet alternative (uncomment if needed)
# router.register('books', views.BookViewSet)
# router.register('authors', views.AuthorViewSet)
# urlpatterns += router.urls