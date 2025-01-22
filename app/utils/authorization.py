from fastapi import APIRouter, Depends, HTTPException, Response

from app.utils.jwt import create_access_token
from database.connect import get_db

from app.entities.user.schema import User, UserLogin, UserRegister
from database.models.user import User as UserDB

from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.hash_password import hash_password, check_password
from app.utils.verification import verify_user


router = APIRouter(tags=['Auth'])


def generate_payload(user: UserDB):
    return {
            "id": user.id,
            "username": user.username,
            "email": user.email  
        }
    
def set_token_in_cookie(response: Response, access_token: str) -> None:
    response.set_cookie(key='access_token',
                        value=access_token,
                        httponly=True,
                        samesite="Strict")


@router.post('/login')
async def auth_user(user: UserLogin,
                    response: Response,
                    session: AsyncSession = Depends(get_db)):
    result = await verify_user(user.username, session=session)

    if result:
        is_correct_password = check_password(user.password, result.hash_password)

        if not is_correct_password:
            raise HTTPException(status_code=401,
                                detail="Неверный логин или пароль")
        
        payload = generate_payload(result)

        access_token = create_access_token(payload=payload)
        set_token_in_cookie(response, access_token)

        return {"access_token": access_token}
    

@router.post('/reg')
async def reg_user(user: UserRegister, response: Response, session: AsyncSession = Depends(get_db)):
    await verify_user(user.username, session=session, is_reg=True)

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

    payload = generate_payload(new_user)

    access_token = create_access_token(payload=payload)
    set_token_in_cookie(response,access_token)
    
    return {"access_token": access_token}
