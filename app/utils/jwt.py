from fastapi import HTTPException, Request
import jwt
from datetime import datetime, timedelta, timezone


from config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES,REFRESH_TOKEN_EXPIRE_DAYS, ALGORITHM


def create_access_token(payload: dict, expire: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=expire)
    payload.update({'exp': expire_time})

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(payload: dict, expire: int = REFRESH_TOKEN_EXPIRE_DAYS):
    expire_time = datetime.now(timezone.utc) + timedelta(days=expire)
    payload.update({'exp': expire_time})

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def check_access_token(request: Request):
    return check_token(request, token_type="access_token")

def check_refresh_token(request: Request):
    return check_token(request, token_type="refresh_token")


def check_token(request: Request, token_type: str):
    token = request.cookies.get(token_type)

    if not token:
        raise HTTPException(status_code=401, detail="The token was not found. Please log in.")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        data = {
                "id": payload.get("id"),
                "username": payload.get("username"),
                "email": payload.get("email"),
            }
          
        if not all(data.values()):
            raise HTTPException(status_code=401, detail="Invalid token payload.")
        return data
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="The token has expired. Please log in again.")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Ivalid token")
    
    
    
        