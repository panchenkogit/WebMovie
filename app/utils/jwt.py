from fastapi import HTTPException, Request
import jwt
from datetime import datetime, timedelta, timezone

from config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM


def create_access_token(payload: dict, expire: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=expire)
    payload.update({'exp': expire_time})

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def check_access_token(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="The token was not found. Please log in.")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        data = {"id": payload.get("id"),
                "username": payload.get("username"),
                "email": payload.get("email")}
        
        if not all(data.values()):
            raise HTTPException(status_code=401, detail="Invalid token payload.")
        
        return data
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="The token has expired. Please log in again.")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Ivalid token")
    
    
