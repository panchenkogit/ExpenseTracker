from typing import List
from fastapi import APIRouter, Depends, HTTPException
from dateutil.relativedelta import relativedelta 
from database.connect import AsyncSession, get_session
from database.entities import Sub as SubDB

import datetime

from subscriber_servise.models import Sub, SubCreate, SubUpdate

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from common_utils.utils.auth import get_current_user

router = APIRouter(prefix="/sub",
                   tags=["Subs"])
TIMESPANS = {
    1:{"days":1},
    2:{"weeks":1},
    3:{"months":1},
    4:{"years":1}
}


def сounting_payment_day(frequency_id: int, start_date: datetime.date)->datetime.date:
    if frequency_id not in TIMESPANS:
        raise ValueError("Некорректный frequency_id")
    return start_date + relativedelta(**TIMESPANS[frequency_id])


@router.get("/get_all_subs", response_model=List[Sub], status_code=200)
async def get_user_subs(current_user: dict = Depends(get_current_user),
                        session: AsyncSession = Depends(get_session)) -> List[Sub]:
    query = await session.execute(select(SubDB).options(joinedload(SubDB.frequency)).
                                  where(SubDB.user_id == current_user['user_id']))
    
    result = query.scalars().all()
    if not result:
        return []
    
    return result


@router.post("/create_new_sub", response_model=Sub, status_code=201)
async def create_new_sub(sub: SubCreate,
                        current_user: dict = Depends(get_current_user),
                        session: AsyncSession = Depends(get_session)) -> Sub:
    """ID частоты платежей (1 - ежедневно, 2 - еженедельно,3 - ежемесячно, 4 - ежегодно)"""
    payment_date = сounting_payment_day(sub.frequency_id, sub.start_date)

    new_sub= SubDB(**sub.model_dump(),
                    payment_date=payment_date,
                    user_id=current_user["user_id"])


    session.add(new_sub)
    await session.flush()
    await session.refresh(new_sub, ["frequency"])

    return new_sub


@router.patch('/update/{id}', response_model=Sub)
async def update_sub(sub_id: int,
                    update_data: SubUpdate,
                    current_user: dict = Depends(get_current_user),
                    session: AsyncSession = Depends(get_session)) -> Sub:
    query = await session.execute(select(SubDB).
                                  where(SubDB.id == sub_id, SubDB.user_id == current_user['user_id']))
    result = query.scalar_one_or_none()

    if result is None:
        raise HTTPException(status_code=404,
                            detail="Not Found!")
    
    sub = update_data.model_dump(exclude_unset=True)

    for key, value in sub.items():
        if value is not None:
            setattr(result, key, value)

    await session.flush()
    await session.refresh(result, ["frequency"])

    return result
    

@router.delete('/delete/{id}', status_code=204)
async def delete_sub(sub_id: int,
                    current_user: dict = Depends(get_current_user),
                    session: AsyncSession = Depends(get_session)):
    query = await session.execute(select(SubDB).
                                  where(SubDB.id == sub_id, SubDB.user_id == current_user['user_id']))
    result = query.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=404,
                            detail="Not Found!")
    
    await session.delete(result)

    return {"message": "Deleted"}