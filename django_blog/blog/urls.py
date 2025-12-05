from django.urls import path
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, 
    PostUpdateView, PostDeleteView
)

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/comment/', views.post_detail_view, name='post_detail'),
    path('comment/<int:pk>/update/', views.comment_update_view, name='comment_update'),
    path('comment/<int:pk>/delete/', views.comment_delete_view, name='comment_delete'),
     path('search/', views.search_view, name='search'),
    path('tags/<slug:tag_slug>/', views.tag_view, name='tag_posts'),
]