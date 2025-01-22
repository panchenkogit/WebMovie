from fastapi import Depends, HTTPException

from database.connect import get_db

from database.models.user import User as UserDB

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select



async def verify_user(username: str, session: AsyncSession = Depends(get_db)) -> None:
    query = await session.execute(select(UserDB).where(UserDB.username == username))
    result = query.scalar_one_or_none()

    if result is not None:
        raise HTTPException(status_code=400,
                            detail="User already exists!")

    return