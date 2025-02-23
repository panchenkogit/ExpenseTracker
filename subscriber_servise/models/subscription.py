from pydantic import BaseModel, Field
import datetime

from typing import Optional

from subscriber_servise.models import FrequencyBase

class SubBase(BaseModel):
    title: str = Field(..., description="Название подписки")
    start_date: datetime.date = Field(..., description="Дата начала подписки")
    cost: int = Field(..., description="Стоимость подписки")

class SubCreate(SubBase):
    frequency_id: int = Field(...,gt=0, lt=5,
                              description="ID частоты платежей (1 - ежедневно, 2 - еженедельно,3 - ежемесячно, 4 - ежегодно)")
    

class SubUpdate(SubBase):
    title: Optional[str] = None
    start_date: Optional[datetime.date] = None
    cost: Optional[int] = None
    frequency_id: Optional[int] = Field(None,gt=0, lt=5,
                              description="ID частоты платежей (1 - ежедневно, 2 - еженедельно,3 - ежемесячно, 4 - ежегодно)")


class Sub(SubBase):
    id: int = Field(..., description="Уникальный идентификатор записи")
    payment_date: datetime.date = Field(..., description="Дата следующего платежа")
    frequency: FrequencyBase

    class Config:
        from_attributes = True
