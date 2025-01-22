from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import NonNegativeInt



from app.utils.jwt import create_access_token
from database.connect import get_db

from app.entities.user.schema import User, UserLogin, UserRegister
from database.models.user import User as UserDB

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.utils.hash_password import hash_password, check_password
from app.utils.dependencies import verify_user

router = APIRouter(tags=['Auth'])


@router.post('/login')
async def auth_user(user: UserLogin,
                    responce: Response,
                    session: AsyncSession = Depends(get_db)):
    result = await verify_user(user.username, session)

    if result:
        is_correct_password = check_password(user.password, result.hash_password)

        if not is_correct_password:
            raise HTTPException(status_code=401,
                                detail="Неверный логин или пароль")
        
        payload = {
            "id": result.id,
            "username": result.username,
            "email": result.email  
        }

        access_token = create_access_token(payload=payload)
        
        responce.set_cookie(key='access_token', value=access_token, httponly=True)

        return {"access_token": access_token}
