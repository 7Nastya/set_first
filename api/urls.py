from django.urls import path
from .views import (
    CommentDetailApiView,
    PostDetailApiView,
    PostListApiView,
    PostCreateView,
    CommentCreateView
)

urlpatterns = [
    path('post_list', PostListApiView.as_view()),
    path('post_detail/<int:pk>/', PostDetailApiView.as_view()),
    path('post_create', PostCreateView.as_view()),
    path('comment_create', CommentCreateView.as_view()),
    path('comment_detail/<int:pk>/', CommentDetailApiView.as_view()),
]
