from fastapi import APIRouter, Depends, HTTPException

from database.connect import AsyncSession, get_session
from database.entities import User as UserDB

from sqlalchemy import exists, select

from user_service.models import User, RegUser, LoginUser
from user_service.utils.auth import hash_password, check_password


router = APIRouter(prefix="/user",
                   tags=["User Reg login"])


async def check_email(email: str, session: AsyncSession) -> bool:
    query = await session.execute(select(exists().where(UserDB.email == email)))
    return query.scalar()

@router.post("/register")
async def reg_user(user: RegUser,
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
    