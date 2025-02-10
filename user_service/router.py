from fastapi import APIRouter, Depends, HTTPException, Response

from database.connect import AsyncSession, get_session
from database.entities import User as UserDB

from sqlalchemy import exists, select

from user_service.models import User, RegUser, LoginUser
from user_service.utils.auth import hash_password, check_password
from user_service.utils.cookies import set_token_in_cookie
from user_service.utils.jwt import create_access_token, get_payload


router = APIRouter(prefix="/user",
                   tags=["User Reg login"])


async def check_email(email: str, session: AsyncSession) -> bool:
    query = await session.execute(select(exists().where(UserDB.email == email)))
    return query.scalar()

@router.post("/register")
async def register(user: RegUser,
                   session: AsyncSession = Depends(get_session)):
    if await check_email(user.email, session):
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует!")

    password_hash = hash_password(user.password)

    new_user = UserDB(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        birth=user.birth,
        password_hash=password_hash
    )
    session.add(new_user)
    
    raise HTTPException(status_code=200,
                         detail="Вы успешно зарегистрировались!")

@router.post("/login")
async def login(user: LoginUser,
                responce: Response,
                session: AsyncSession = Depends(get_session)):
    if not await check_email(user.email, session):
        raise HTTPException(status_code=400,
                            detail="Пользователя с таким email не существует!")
    
    query = await session.execute(select(UserDB).where(UserDB.email == user.email))
    result = query.scalar_one_or_none()
    if not check_password(user.password, result.password_hash):
        raise HTTPException(status_code=400,
                            detail="Неправильный логин или пароль")
    
    payload = get_payload(result)
    access_token = create_access_token(payload)
    set_token_in_cookie(responce, access_token)

    return {"access_token": access_token}


    