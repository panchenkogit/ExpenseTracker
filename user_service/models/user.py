from pydantic import BaseModel, Field, EmailStr

import datetime


class BaseUser(BaseModel):
    firstname: str = Field(..., min_length=2, max_length=50, description="")
    lastname: str = Field(..., min_length=2, max_length=50, description="")
    email: EmailStr = Field(..., min_length=2, max_length=50, description="")
    birth: datetime.date | None = None


class RegUser(BaseUser):
    password: str = Field(..., min_length=4, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")


class User(BaseUser):
    id: int = Field(..., ge=1, description="")


class LoginUser(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор записи")
    email: EmailStr = Field(..., min_length=2, max_length=50, description="")
    password: str = Field(..., min_length=4, max_length=20)

    class Config:
        from_attributes = True
