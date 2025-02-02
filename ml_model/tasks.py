from database.connect import get_sync_db
from train_model import train_surprise_model

from app.utils.celery_config import celery

@celery.task
def daily_retraining():
    session = next(get_sync_db())
    try:
        train_surprise_model(session)
        print("Модель переобучена.")
    finally:
        session.close()
