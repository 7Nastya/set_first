from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(models.Model):
    username = models.CharField(max_length=25, verbose_name="Ник")
    birthday = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    date_joined = models.DateTimeField(max_length=30, blank=True, verbose_name="Дата присоединения")
    email = models.EmailField(max_length=40, verbose_name="Адрес элктронной почты")
    first_name = models.CharField(max_length=20, verbose_name="Имя")
    last_name = models.CharField(max_length=20, verbose_name="Фамилия")
