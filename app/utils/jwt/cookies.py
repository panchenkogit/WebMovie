from fastapi import Response

from app.utils.jwt.jwt import create_access_token, create_refresh_token

from database.models.user import User as UserDB


def generate_payload(user: UserDB) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }


def create_tokens(payload: dict) -> dict:
    access_token = create_access_token(payload=payload)
    refresh_token = create_refresh_token(payload=payload)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


def set_token_in_cookie(response: Response, tokens: dict) -> None:
    for token_name, token_item in tokens.items():
        response.set_cookie(
            key=token_name,
            value=token_item,
            httponly=True,
            samesite="Strict",
        )


