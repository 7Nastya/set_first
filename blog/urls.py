from django.urls import path, re_path
from . import views
# from .views import PostView
# app_name = "post"
# from .views import PostListView

urlpatterns = [
    path('', views.post_list, name='post_list'),
    # path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    # path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/new/', views.PostNew.as_view(), name='post_new'),
    # path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('login/', views.user_login, name='login'),
    # path('exit/', views.LogoutView.as_view(), name='exit'),
    # path('post/account', views.user_login, name='login'),
    # path('post/', PostView.as_view()),
]