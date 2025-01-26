from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response

from app.entities.film.schema import Film, FilmUpdate
from database.models.film import Film as FilmDB
from database.models.relationships import UserFilmLibrary
from app.utils.jwt import check_access_token
from database.connect import get_db


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select, exists



router = APIRouter(prefix='/film',
                   tags=['Films'])



    
@router.get('/all', response_model=List[Film])
async def get_all_films(session: AsyncSession = Depends(get_db)) -> List[Film]:

    query = await session.execute(select(FilmDB))
    result = query.scalars().all()

    return result


@router.patch("/edit_film/{film_id}", response_model=Film)
async def edit_film(film_id: int,
                    film_update: FilmUpdate,
                    current_user: dict = Depends(check_access_token),
                    session: AsyncSession = Depends(get_db)) -> Film:
    
    query = await session.execute(select(FilmDB).where(FilmDB.id == film_id))
    film = query.scalar_one_or_none()

    if not film:
        raise HTTPException(status_code=404, detail="Film not found!")

    for key, value in film_update.model_dump(exclude_unset=True).items():
        setattr(film, key, value)

    await session.commit()
    await session.refresh(film)

    return film

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

    


@router.get("/get_by_id/{id}", response_model=Film)
async def get_film_by_id(id: int,
                         session: AsyncSession = Depends(get_db)) -> Film:
    
    query = await session.execute(select(FilmDB).where(FilmDB.id == id))
    result = query.scalar_one_or_none()

    if result is None:
        raise HTTPException(status_code=404,
                            detail="Not found!")
    return result


@router.delete("/delete_by_id/{film_id}")
async def delete_film(film_id: int,
                      current_user: dict = Depends(check_access_token),
                      session: AsyncSession = Depends(get_db)) -> Response:
    
    query = await session.execute(select(FilmDB).where(FilmDB.id == film_id))
    film = query.scalar_one_or_none()

    if not film:
        raise HTTPException(status_code=404, detail="Film not found!")

    await session.delete(film)
    await session.commit()

    return Response(status_code=204)


