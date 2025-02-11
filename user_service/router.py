from fastapi import APIRouter, Depends, HTTPException, Response

from database.connect import AsyncSession, get_session
from database.entities import User as UserDB

from sqlalchemy import exists, select

from user_service.models import User, RegUser, LoginUser
from user_service.utils.auth import hash_password, check_password
from user_service.utils.cookies import set_tokens_in_cookie
from user_service.utils.jwt import create_tokens, get_payload


router = APIRouter(prefix="/user",
                   tags=["User Reg login"])


async def check_email(email: str, session: AsyncSession) -> bool:
    query = await session.execute(select(exists().where(UserDB.email == email)))
    return query.scalar_one()

@router.post("/register")
async def register(user: RegUser,
                   response: Response,
                   session: AsyncSession = Depends(get_session)):
    if await check_email(user.email, session):
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует.")

    password_hash = hash_password(user.password)

    new_user = UserDB(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        birth=user.birth,
        password_hash=password_hash
    )
    session.add(new_user)

    payload = get_payload(new_user)
    tokens  = create_tokens(payload)
    set_tokens_in_cookie(response, tokens)
    
    return {"detail": "Вы успешно зарегистрировались!"}


@router.post("/login")
async def login(user: LoginUser,
                response: Response,
                session: AsyncSession = Depends(get_session)):
    if not await check_email(user.email, session):
        raise HTTPException(status_code=404,
                            detail="Пользователя с таким email не существует!")
    
    query = await session.execute(select(UserDB).where(UserDB.email == user.email))
    result = query.scalar_one_or_none()
    if not check_password(user.password, result.password_hash):
        raise HTTPException(status_code=401,
                            detail="Неправильный логин или пароль")
    
    payload = get_payload(result)

    tokens  = create_tokens(payload)
    set_tokens_in_cookie(response, tokens)

    return {"detail": "Вы успешно вошли."}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")


    