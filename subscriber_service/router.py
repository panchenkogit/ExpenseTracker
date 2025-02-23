from datetime import timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from common_utils.utils.calculate_payday import сounting_payment_day, date_to_timestamp
from database.connect import AsyncSession, get_session
from database.entities import Sub as SubDB

from common_utils.redis.cache_sub import add_reminder, remove_reminder


from subscriber_service.models import Sub, SubCreate, SubUpdate

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from common_utils.utils.auth import get_current_user

router = APIRouter(prefix="/sub",
                   tags=["Subs"])


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
    """ID частоты платежей (1 - ежедневно, 2 - еженедельно, 3 - ежемесячно, 4 - ежегодно)"""
    # Дата следующего платежа
    payment_date = сounting_payment_day(sub.frequency_id, sub.start_date)

    new_sub = SubDB(**sub.model_dump(),
                    payment_date=payment_date,
                    user_id=current_user["user_id"])

    session.add(new_sub)
    await session.flush()
    await session.refresh(new_sub, ["frequency"])

    # Добавляем напоминание в Redis за 3 дня до платежа
    notify_date = payment_date - timedelta(days=3)
    timestamp = date_to_timestamp(notify_date)

    # Добавляем напоминание в Redis
    await add_reminder(
        email=current_user['email'],
        sub_title=new_sub.title,
        reminder_date=timestamp,
        frequency_id=sub.frequency_id
    )

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
    
    #remove reminder in redis
    await remove_reminder(current_user['email'],
                          result.title,
                          result.frequency_id)
    
    sub = update_data.model_dump(exclude_unset=True)

    for key, value in sub.items():
        if value is not None:
            setattr(result, key, value)

    await session.flush()
    await session.refresh(result, ["frequency"])


    await add_reminder(current_user['email'],
                       result.title,
                        date_to_timestamp(result.payment_date),
                        result.frequency_id)
    

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
    await remove_reminder(current_user['email'],
                          result.title,
                          result.frequency_id)

    return {"message": "Deleted"}