import pickle
from celery import shared_task
from ml_model.train_model import train_surprise_model
from database.connect import sync_session  # Используем синхронную сессию

@shared_task
def retrain_model():
    """
    Celery-задача для переобучения модели рекомендаций.
    """
    # Используем синхронную сессию
    with sync_session() as session:
        model = train_surprise_model(session)  # Теперь эта функция работает синхронно
        with open("ml_model/svd_model.pkl", "wb") as f:
            pickle.dump(model, f)
        print("Модель переобучена и сохранена.")
