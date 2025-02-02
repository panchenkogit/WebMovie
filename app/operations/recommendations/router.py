from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.jwt import check_access_token

from database.models import Film as FilmDB
from database.connect import get_db
from database.models.relationships import UserFilmLibrary
from ml_model.als_recommender import load_model


router = APIRouter(prefix='/recomend',
                   tags=['recommendations'])


@router.get("/recommendations/{user_id}")
async def get_recommendations(session: AsyncSession = Depends(get_db),
                              current_user: dict = Depends(check_access_token)):
    model = load_model()

    result = await session.execute(select(FilmDB.id))
    film_ids = result.scalars().all()

    predictions = [(film_id, model.predict(current_user["id"], film_id).est) for film_id in film_ids]
    predictions.sort(key=lambda x: x[1], reverse=True)
    top_films = [film_id for film_id, _ in predictions[:10]]
    
    return {"user_id": current_user["id"], "recommended_films": top_films}


async def get_user_film_rating(user_id: int,
                               film_id: int,
                               session: AsyncSession):
    query = await session.execute(
        select(UserFilmLibrary).where(
            UserFilmLibrary.user_id == user_id,
            UserFilmLibrary.film_id == film_id,
        )
    )
    return query.scalars().first()


@router.post('/rate_film/{film_id}')
async def rate_film(film_id: int,
                    rating: float,
                    session: AsyncSession = Depends(get_db),
                    current_user: dict = Depends(check_access_token)):
    
    if rating < 0 or rating > 10:
        raise HTTPException(status_code=400, detail="Оценка должна быть от 0 до 10") 
    
    user_film = await get_user_film_rating(current_user["id"], film_id, session)

    if user_film:
        user_film.user_rating = rating

    else:
        user_film = UserFilmLibrary(
            user_id=current_user['id'],
            film_id=film_id,
            user_rating=rating
        )
        session.add(user_film)
    
    try:
        await session.commit()
        return {"detail": "Оценка успешно сохранена"}
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Ошибка сохранения оценки")
    

@router.delete("/delete_rating")
async def delete_rating(
    film_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_access_token),
):
    
    user_film = await get_user_film_rating(current_user["id"], film_id, session)

    if not user_film:
        raise HTTPException(status_code=404, detail="Оценка не найдена")

    await session.delete(user_film)
    await session.commit()

    return {"detail": "Оценка удалена"}

