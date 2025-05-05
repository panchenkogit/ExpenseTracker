from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.connect import Base


class Frequency(Base):
    __tablename__ = "frequencies"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, index=True, nullable=False)

    subscriptions = relationship("Sub", back_populates="frequency")
