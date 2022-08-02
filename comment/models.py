from django.db import models
from django.utils import timezone

from blog.models import Post
from my_user.models import MyUser


class Comment(models.Model):
    post = models.ForeignKey(Post, default=None, null=True, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(MyUser, default=None, null=True, on_delete=models.CASCADE, related_name='user_name')
    content = models.TextField(verbose_name='Содержание')
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['created_date']

    def __str__(self):
        return self.content