from celery import Celery
from celery.schedules import crontab

celery = Celery("webmovie_tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

celery.conf.update(timezone="UTC")

celery.conf.beat_schedule = {
    "retrain_every_minute": {
        "task": "app.utils.celery.tasks.retrain_model",  # Убедись, что путь правильный!
        "schedule": 60.0  # Каждую минуту
    },
}
