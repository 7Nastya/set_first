from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'foto', 'created_date', 'published_date')
    list_display = ('id', 'title')
    list_filter = ('published_date', 'created_date')

admin.site.register(Post, PostAdmin)