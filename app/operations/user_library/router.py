from fastapi import APIRouter, Depends, HTTPException

from database.models.film import Film as FilmDB
from database.models.relationships import UserFilmLibrary
from database.connect import get_db

from app.utils.jwt.jwt import check_access_token

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select, exists



router = APIRouter(prefix='/user_library',
                   tags=['Library'])


@router.get("/all_like_film")
async def get_all_like_film(session: AsyncSession = Depends(get_db),
                            current_user: dict = Depends(check_access_token)):
    result = await session.execute(select(UserFilmLibrary.film_id, UserFilmLibrary.user_rating)
                                   .where(UserFilmLibrary.user_id == current_user['id']))
    data = result.all()
    if not data:
        raise HTTPException(status_code=404, detail="Films not found!")

    return [{"film_id": film_id, "rating": rating} for film_id, rating in data]


@router.post("/add_film_in_library/{film_id}")
async def add_film_in_library(film_id: int,
                              session: AsyncSession = Depends(get_db),
                              current_user: dict = Depends(check_access_token)):
    
    film_exists_query = await session.execute(
        select(exists().where(FilmDB.id == film_id))
    )
    film_exists = film_exists_query.scalar()

    if not film_exists:
        raise HTTPException(status_code=404, detail="Film not found!")


    in_library_query = await session.execute(
        select(exists().where(
            and_(
                UserFilmLibrary.user_id == current_user['id'],
                UserFilmLibrary.film_id == film_id
            )
        ))
    )

    in_library = in_library_query.scalar()

    if in_library:
        return {"detail": "Film is already in your library!"}

    new_like_film = UserFilmLibrary(
        user_id=current_user['id'],
        film_id=film_id
    )
    try:

        session.add(new_like_film)
        await session.commit()

        return {"detail": "Film added to library"}
    except:

        session.rollback()
        return {"detail": "Что то пошло не так"}
    

@router.delete("/delete_film_in_library/{film_id}")
async def delete_film_in_library(film_id: int,
                                session: AsyncSession = Depends(get_db),
                                current_user: dict = Depends(check_access_token)):
    
    film_exists_query = await session.execute(
        select(exists().where(FilmDB.id == film_id))
    )
    film_exists = film_exists_query.scalar()

    if not film_exists:
        raise HTTPException(status_code=404, detail="Film not found!")


    in_library_query = await session.execute(
        select(UserFilmLibrary).where(
                UserFilmLibrary.user_id == current_user['id'],
                UserFilmLibrary.film_id == film_id
            )
        )

    in_library = in_library_query.scalar()

    if not in_library:
        return {"Этого фильма нет в вашей библиотеке"}
    
    try:
        await session.delete(in_library)
        await session.commit()
        return {"detail": "Film removed from your library!"}
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Something went wrong!") from e
    

