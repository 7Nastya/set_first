from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/new/', views.PostNew.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.PostEdit.as_view(), name='post_edit'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('accounts/profile/<int:pk>', views.profile, name='profile'),
    path('accounts/profile/<int:pk>/edit/', views.ChangeUserInfoView.as_view(), name='profile_edit'),
    path('accounts/logout/', views.UserLoginOut.as_view(), name='logout'),
]
