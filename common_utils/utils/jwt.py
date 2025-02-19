from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Response
import jwt

from config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, REFRESH_TOKEN_EXPIRE_DAYS

from database.entities import User as UserDB

def add_payload(user: UserDB) -> dict:
    return {
        "user_id": user.id,
        "user_uuid": str(user.uuid),
        "email": user.email,
        "firstname": user.firstname
    }

def get_payload(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен истёк")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Неверный токен")

def create_tokens(payload: dict):
    return {
            "access_token" : create_access_token(payload),
            "refresh_token": create_refresh_token(payload)
            }

def create_access_token(payload: dict):
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    payload.update({'exp': expire_time})

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(payload: dict):
    expire_time = datetime.now(timezone.utc) + timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))
    payload.update({'exp': expire_time})

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    