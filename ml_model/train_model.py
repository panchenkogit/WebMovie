import pandas as pd
from sqlalchemy.orm import Session
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
from database.models import UserFilmLibrary

def get_ratings_data(session: Session) -> pd.DataFrame:
    result = session.query(UserFilmLibrary).all()
    
    rows = []
    for record in result:
        if record.user_rating is not None:
            rows.append({
                'user_id': record.user_id,
                'film_id': record.film_id,
                'rating': record.user_rating
            })
    
    df = pd.DataFrame(rows)
    return df


def train_surprise_model(session: Session):
    df = get_ratings_data(session)
    print(f"Получено {len(df)} записей оценок")

    reader = Reader(rating_scale=(1, 10))
    
    data = Dataset.load_from_df(df[['user_id', 'film_id', 'rating']], reader)
    
    trainset, testset = train_test_split(data, test_size=0.2)
    
    model = SVD()
    model.fit(trainset)

    predictions = model.test(testset)
    rmse = accuracy.rmse(predictions)
    print(f"RMSE модели: {rmse}")
    
    return model
