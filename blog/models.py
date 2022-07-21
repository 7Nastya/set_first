from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    # slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    text = models.TextField(blank=True, verbose_name="Текст статьи")
    foto = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name="Фото")
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Время создания")
    published_date = models.DateTimeField(blank=True, null=True, verbose_name="Время публикации")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Герои"
        verbose_name_plural = "Герои"
        ordering = ['created_date', 'title']
