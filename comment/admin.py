from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'content', 'created_date')


admin.site.register(Comment, CommentAdmin)
