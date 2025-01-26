from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response

from app.entities.directors.schema import Director, DirectorUpdate
from app.utils.jwt import check_access_token
from database.connect import get_db

from database.models.director import Director as DirectorDB

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select



router = APIRouter(prefix='/director',
                   tags=['Directors'])


@router.get('/all', response_model=List[Director])
async def get_all_directors(session: AsyncSession = Depends(get_db)) -> List[Director]:
    query = await session.execute(select(DirectorDB))
    result = query.scalars().all()
    return result


@router.get("/{id}", response_model=Director)
async def get_director_by_id(id: int,
                             session: AsyncSession = Depends(get_db)) -> Director:
    query = await session.execute(select(DirectorDB).where(DirectorDB.id == id))
    result = query.scalar_one_or_none()

    if result is None:
        raise HTTPException(status_code=404,
                            detail="Director not found!")
    return result


@router.post("/", response_model=Director, status_code=201)
async def create_director(director: Director,
                          current_user: dict = Depends(check_access_token),
                          session: AsyncSession = Depends(get_db)) -> Director:
    
    new_director = DirectorDB(**director.model_dump())
    session.add(new_director)
    await session.commit()
    await session.refresh(new_director)
    return new_director


@router.patch("/{id}", response_model=Director)
async def update_director(id: int,
                          director_update: DirectorUpdate,
                          current_user: dict = Depends(check_access_token),
                          session: AsyncSession = Depends(get_db)) -> Director:
    
    query = await session.execute(select(DirectorDB).where(DirectorDB.id == id))
    director = query.scalar_one_or_none()

    if not director:
        raise HTTPException(status_code=404, detail="Director not found!")

    for key, value in director_update.model_dump(exclude_unset=True).items():
        setattr(director, key, value)

    await session.commit()
    await session.refresh(director)
    return director


@router.delete("/{id}")
async def delete_director(id: int,
                          current_user: dict = Depends(check_access_token),
                          session: AsyncSession = Depends(get_db)) -> Response:
    
    query = await session.execute(select(DirectorDB).where(DirectorDB.id == id))
    director = query.scalar_one_or_none()

    if not director:
        raise HTTPException(status_code=404, detail="Director not found!")

    await session.delete(director)
    await session.commit()

    return Response(status_code=204)