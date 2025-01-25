from fastapi import Depends, HTTPException

from app.entities.user.schema import User
from database.connect import get_db

from database.models.user import User as UserDB

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select



async def verify_user(username: str, session: AsyncSession = Depends(get_db), is_reg: bool = False) -> UserDB:
    query = await session.execute(select(UserDB).where(UserDB.username == username))
    result = query.scalar_one_or_none()

    if is_reg:
        if result:
            raise HTTPException(status_code=400,
                            detail="User already exists!")
        return
        

    if not is_reg and result is None:
        raise HTTPException(status_code=401,
                            detail="Неверный логин или пароль")  

    return result

