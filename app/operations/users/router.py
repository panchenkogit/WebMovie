from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import NonNegativeInt

from app.utils.jwt.cookies import create_tokens, generate_payload, set_token_in_cookie
from app.utils.jwt.jwt import check_access_token
from database.connect import get_db

from app.entities.user.schema import User, UserLogin, UserRegister, UserUpdate
from database.models.user import User as UserDB

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.utils.auth.hash_password import hash_password, check_password
from app.utils.auth.verification import verify_user


router = APIRouter(prefix="/users",
                   tags=["Users"])


@router.get("/all", response_model=List[User])
async def get_all_users(page: int = 1,
                        per_page: int = 20,
                        session: AsyncSession = Depends(get_db)) -> List[User]:
    offset = (page - 1) * per_page

    query = await session.execute(select(UserDB).limit(per_page).offset(offset))
    
    result = query.scalars().all()
    return result



@router.get("/{id}", response_model=User)
async def get_user_by_id(id: int,
                         session: AsyncSession = Depends(get_db)) -> User:
    
    query = await session.execute(select(UserDB).where(UserDB.id == id))
    result = query.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=404,
                            detail="Not found!")
    return result



@router.patch("/edit_user")
async def edit_user(user_update: UserUpdate,
                    response: Response,
                    current_user: dict = Depends(check_access_token),
                    session: AsyncSession = Depends(get_db)) -> User:

    if user_update.username and user_update.username != current_user["username"]:
        await verify_user(user_update.username, session=session, is_reg=True)

    if user_update.password:
        user_update.password = hash_password(user_update.password)

    user = await session.get(UserDB, current_user["id"])
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")


    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    await session.commit()
    await session.refresh(user)
    

    payload = generate_payload(user=user)
    if payload != current_user:
        tokens = create_tokens(payload=payload)
        set_token_in_cookie(response, tokens)
    
    return user


        