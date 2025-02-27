from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.jwt.cookies import generate_payload,create_tokens, set_token_in_cookie
from app.utils.jwt.jwt import check_token, create_access_token, create_refresh_token
from app.utils.auth.hash_password import hash_password, check_password
from app.utils.auth.verification import verify_user

from database.connect import get_db
from database.models.user import User as UserDB

from app.entities.user.schema import UserLogin, UserRegister


router = APIRouter(tags=["Auth"])


@router.post("/login")
async def auth_user(
    user: UserLogin,
    response: Response,
    session: AsyncSession = Depends(get_db),
):
    result = await verify_user(user.username, session=session)
    if not result:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    is_correct_password = check_password(user.password, result.hash_password)
    if not is_correct_password:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    payload = generate_payload(result)
    tokens = create_tokens(payload=payload)
    set_token_in_cookie(response, tokens)

    return {"access_token": tokens.get("access_token")}


@router.post("/reg")
async def reg_user(
    user: UserRegister,
    response: Response,
    session: AsyncSession = Depends(get_db),
):
    await verify_user(user.username, session=session, is_reg=True)

    hash_pass = hash_password(user.password)

    new_user = UserDB(
        username=user.username,
        hash_password=hash_pass,
        age=user.age,
        email=user.email,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    payload = generate_payload(new_user)
    tokens = create_tokens(payload=payload)
    set_token_in_cookie(response, tokens)

    return tokens


@router.post("/logout")
def log_out(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"detail": "Logged out successfully"}


@router.post("/refresh_token")
def refresh_token(request: Request, response: Response):
    payload = check_token(request, token_type="refresh_token")

    tokens = create_tokens(payload=payload)
    set_token_in_cookie(response, tokens)

    return {"access_token": tokens.get("access_token")}

