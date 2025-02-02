import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models import User, Film, UserFilmLibrary, FilmDirector, FilmGenre
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
import asyncio
from database.connect import async_session 
import pickle

async def get_ratings_data(session: AsyncSession) -> pd.DataFrame:
    result = await session.execute(select(UserFilmLibrary))
    data = result.scalars().all()

    rows = []
    for record in data:
        if record.user_rating is not None:
            rows.append({
                'user_id': record.user_id,
                'film_id': record.film_id,
                'rating': record.user_rating
            })
    
    df = pd.DataFrame(rows)
    return df


async def train_surprise_model(session: AsyncSession):
    df = await get_ratings_data(session)
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


if __name__ == "__main__":
    

    async def main():
        async with async_session() as session:
            model = await train_surprise_model(session)
            
            with open("ml_model/svd_model.pkl", "wb") as f:
                pickle.dump(model, f)
            print("Модель обучена и сохранена.")

    asyncio.run(main())
