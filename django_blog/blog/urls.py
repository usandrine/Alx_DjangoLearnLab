from django.urls import path
from . import views
from .views import (
    CommentCreateView, CommentDeleteView, CommentUpdateView, PostListView, PostDetailView, PostCreateView, 
    PostUpdateView, PostDeleteView
)

urlpatterns = [
  path('', PostListView.as_view(), name='post_list'),
    
    # Authentication URLs - must be exactly these
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    
    # Post URLs
     path('posts/<int:post_id>/comments/new/', 
         CommentCreateView.as_view(), 
         name='comment_create'),
    path('comments/<int:pk>/update/', 
         CommentUpdateView.as_view(), 
         name='comment_update'),
    path('comments/<int:pk>/delete/', 
         CommentDeleteView.as_view(), 
         name='comment_delete'),
         path('posts/<int:post_id>/comments/new/', 
     CommentCreateView.as_view(), 
     name='comment_create'),
]