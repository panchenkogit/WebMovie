from celery import Celery
from celery.schedules import crontab
from config import REDIS_URL


celery = Celery("webmovie_tasks", broker=REDIS_URL, backend=REDIS_URL)

celery.conf.update(timezone="UTC")

celery.conf.beat_schedule = {
    "retrain_every_minute": {
        "task": "app.utils.celery.tasks.retrain_model",  # Убедись, что путь правильный!
        "schedule": 60.0  # Каждую минуту
    },
}
