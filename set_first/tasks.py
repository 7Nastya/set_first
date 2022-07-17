# tasks.py
# Импортируем созданный нами ранее экземпляр класса celery(app)
from set_first.celery import app

# Декоратор @app.task, говорит celery о том, что эта функция является (task-ом) т.е. должна выполнятся в фоне.
@app.task
def supper_sum(x, y):
    return x + y