from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.jwt import check_access_token

from database.connect import get_db
from database.models.relationships import UserFilmLibrary


router = APIRouter(prefix='/recomend',
                   tags=['recommendations'])


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

