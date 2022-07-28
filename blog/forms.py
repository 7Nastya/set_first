from django import forms

from my_user.models import MyUser
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ChangeUserInfoForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('username', 'birthday', 'date_joined', 'email', 'first_name', 'last_name')

class SignUpForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password1', 'password2', 'birthday', 'first_name', 'last_name' )
