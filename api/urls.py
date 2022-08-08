from django.urls import path, include
from .views import (
PostCreateSerializer,
CommentCreateSerializer,
CommentSerializer,
CommentDetailApiView,
CommentListApiView,
PostDetailApiView,
PostListApiView,
PostSerializer,
PostCreateView,
CommentCreateView
)

urlpatterns = [
    path('post_list', PostListApiView.as_view()),
    path('post_detail/<int:pk>/', PostDetailApiView.as_view()),
    path('post_create/<int:pk>/', PostCreateView.as_view()),
    path('comment_create/<int:pk>/', CommentCreateView.as_view()),
    path('comment_detail/<int:pk>/', CommentDetailApiView.as_view()),
    path('comment_list/<int:pk>/', CommentListApiView.as_view()),
]