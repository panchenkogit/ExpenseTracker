import bcrypt
from fastapi import HTTPException, Request

from common_utils.utils.jwt import get_payload


def hash_password(password: str) -> str:
    hash_pass = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12))
    return hash_pass.decode("utf-8")


def check_password(password: str, hashed_pass: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_pass.encode("utf-8"))


def get_current_user(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Токен не найден")

    return get_payload(token)
