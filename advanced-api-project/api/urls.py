from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for optional ViewSets
router = DefaultRouter()
router.register(r'books-viewset', views.BookViewSet, basename='book-viewset')
router.register(r'authors-viewset', views.AuthorViewSet, basename='author-viewset')

urlpatterns = [
    # Book endpoints (generic views)
    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', views.BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
    
    # Author endpoints (generic views)
    path('authors/', views.AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', views.AuthorRetrieveUpdateDestroyView.as_view(), name='author-detail'),
    
    # Custom endpoints
    path('statistics/', views.BookStatisticsView.as_view(), name='book-statistics'),
    path('authors/<int:author_id>/books/', views.AuthorBooksView.as_view(), name='author-books'),
    
    # API documentation and authentication
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Include router URLs (optional ViewSets)
    path('', include(router.urls)),
]