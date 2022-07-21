from django.contrib import admin
from .models import MyUser


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username')


admin.site.register(MyUser, MyUserAdmin)
