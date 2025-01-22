from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import NonNegativeInt

from database.connect import get_db

from app.entities.user.schema import User, UserLogin, UserRegister
from database.models.user import User as UserDB

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.utils.hash_password import hash_password, check_password
from app.utils.dependencies import verify_user


router = APIRouter(prefix="/users",
                   tags=["Users"])


@router.get("/all", response_model=List[User])
async def get_all_users(session: AsyncSession = Depends(get_db)) -> List[User]:
    query = await session.execute(select(UserDB))
    result = query.scalars().all()
    if not result:
        raise HTTPException(status_code=404,
                            detail="Not found!")
    return result


@router.get("/{id}", response_model=User)
async def get_user_by_id(id: int, session: AsyncSession = Depends(get_db)) -> User:
    query = await session.execute(select(UserDB).where(UserDB.id == id))
    result = query.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=404,
                            detail="Not found!")
    return result


@router.post("/create", response_model=User)
async def create_user(user: UserRegister, session: AsyncSession = Depends(get_db)) -> User:
    await verify_user(user.username, session)

    hash_pass = hash_password(user.password).decode()

    new_user = UserDB(
        username=user.username,
        hash_password=hash_pass,
        age=user.age,
        email=user.email
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    
    return new_user

@router.patch("")


    
        