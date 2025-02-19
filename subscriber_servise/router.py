from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response

from database.connect import AsyncSession, get_session
from database.entities import User as UserDB
from database.entities import Sub as SubDB

from subscriber_servise.models import Sub

from sqlalchemy import exists, select

from user_service.models import User, RegUser, LoginUser
from common_utils.utils.auth import get_current_user

router = APIRouter(prefix="/sub",
                   tags=["Subs"])

@router.get("/get_all_subs", response_model=List[Sub])
async def get_user_subs(current_user: dict = Depends(get_current_user),
                        session: AsyncSession = Depends(get_session)) -> List[Sub]:
    query = await session.execute(select(SubDB).where(SubDB.user_id == current_user["user_id"]))
    result = query.scalars().all()
    if not result:
        return []
    
    return result
    
