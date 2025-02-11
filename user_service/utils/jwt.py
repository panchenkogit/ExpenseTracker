from datetime import datetime, timedelta, timezone
from fastapi import Response
import jwt

from config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, REFRESH_TOKEN_EXPIRE_DAYS

from database.entities import User as UserDB

def get_payload(user: UserDB) -> dict:
    return {
        "email": user.email,
        "firstname": user.firstname
    }

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
    