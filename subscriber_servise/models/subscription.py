from pydantic import BaseModel, Field, EmailStr

import datetime


from pydantic import BaseModel, Field
import datetime

class SubBase(BaseModel):
    title: str = Field(..., description="Название подписки")
    start_date: datetime.date = Field(..., description="Дата начала подписки")
    cost: int = Field(..., description="Стоимость подписки")

class SubCreate(SubBase):
    frequency_id: int = Field(..., description="ID частоты платежей (1 - ежедневно, 2 - еженедельно,3 - ежемесячно, 4 - ежегодно)")

class Sub(SubBase):
    payment_date: datetime.date = Field(..., description="Дата следующего платежа")
    frequency_id: int = Field(..., description="ID частоты платежей")
