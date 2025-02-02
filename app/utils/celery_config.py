from celery import Celery


celery = Celery('tasks', broker="redis://localhost:6379/0")

celery.conf.beat_schedule = {
    'daily-model-retraining': {
        'task': 'ml_models.tasks.daily_retraining',
        'schedule': 86400.0,
    },
}