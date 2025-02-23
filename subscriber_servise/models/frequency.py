from pydantic import BaseModel

class FrequencyBase(BaseModel):
    title: str

    class Config:
        from_attributes = True