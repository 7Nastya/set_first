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
    path('apii', PostListApiView.as_view()),
    path('apii/<int:pk>/', PostDetailApiView.as_view()),
]