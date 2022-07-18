# tasks.py
# Импортируем созданный нами ранее экземпляр класса celery(app)
import time
from set_first.celery import app

# Декоратор @app.task, говорит celery о том, что эта функция является (task-ом) т.е. должна выполнятся в фоне.
@app.task
def supper_sum(x, y):
    time.sleep(6000)
    print("wait")
    return x + y