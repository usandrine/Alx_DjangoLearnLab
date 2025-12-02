from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for ViewSet
router = DefaultRouter()
router.register(r'books_all', views.BookViewSet, basename='book_all')

urlpatterns = [
    # Task 1: Route for BookList view (ListAPIView)
    path('books/', views.BookList.as_view(), name='book-list'),
    
    # Task 2: Include the router URLs for BookViewSet (all CRUD operations)
    path('', include(router.urls)),
    
    # Task 3: Authentication endpoints
    path('api-token-auth/', views.CustomObtainAuthToken.as_view(), name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]