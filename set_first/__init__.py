# import celery
from set_first.celery import app as celery_app

# Подключаем объект
__all__ = ('celery_app',)
