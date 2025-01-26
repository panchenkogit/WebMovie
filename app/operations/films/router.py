from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response

from app.entities.film.schema import Film, FilmUpdate
from database.models.film import Film as FilmDB
from app.utils.jwt import check_access_token
from database.connect import get_db


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select



router = APIRouter(prefix='/film',
                   tags=['Films'])


@router.get('/all', response_model=List[Film])
async def get_all_films(session: AsyncSession = Depends(get_db)) -> List[Film]:

    query = await session.execute(select(FilmDB))
    result = query.scalars().all()

    return result


@router.get("/{id}", response_model=Film)
async def get_film_by_id(id: int,
                         session: AsyncSession = Depends(get_db)) -> Film:
    
    query = await session.execute(select(FilmDB).where(FilmDB.id == id))
    result = query.scalar_one_or_none()

    if result is None:
        raise HTTPException(status_code=404,
                            detail="Not found!")
    return result

@router.post("/", response_model=Film, status_code=201)
async def create_director(director: Film,
                          current_user: dict = Depends(check_access_token),
                          session: AsyncSession = Depends(get_db)) -> Film:
    
    new_director = FilmDB(**director.model_dump())
    session.add(new_director)
    await session.commit()
    await session.refresh(new_director)
    return new_director


@router.patch("/edit_film", response_model=Film)
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


@router.delete("/{id}")
async def delete_film(id: int,
                      current_user: dict = Depends(check_access_token),
                      session: AsyncSession = Depends(get_db)) -> Response:
    
    query = await session.execute(select(FilmDB).where(FilmDB.id == id))
    film = query.scalar_one_or_none()

    if not film:
        raise HTTPException(status_code=404, detail="Film not found!")

    await session.delete(film)
    await session.commit()

    return Response(status_code=204)
