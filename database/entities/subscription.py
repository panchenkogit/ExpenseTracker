from sqlalchemy import  Column, Date, ForeignKey, Integer, Numeric, String, func
import uuid
from sqlalchemy.orm import relationship
from database.connect import Base


class Sub(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, index=True)
    start_date = Column(Date, server_default=func.now(), nullable=False, index=True)
    cost = Column(Numeric(10, 2), nullable=True)
    frequency_id = Column(Integer, ForeignKey("frequencies.id"), nullable=False)
    payment_date = Column(Date, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True) 

    frequency = relationship("Frequency", back_populates="subscriptions")
    user = relationship("User", back_populates="subscriptions")