from django import forms
from .models import Post
from .models import MyUser
from django.contrib.auth.forms import UserChangeForm

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

#Регистрация пользователей:
# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'email')
#
#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password'] != cd['password2']:
#             raise forms.ValidationError('Passwords don\'t match.')
#         return cd['password2']
#
#
# class LoginForm:
#     pass