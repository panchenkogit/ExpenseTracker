from datetime import datetime, timedelta, timezone
from fastapi import Response
import jwt

from config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM

from database.entities import User as UserDB

def get_payload(user: UserDB) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "firstname": user.firstname
    }

def create_access_token(payload: dict):
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    payload.update({'exp': expire_time})
    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    