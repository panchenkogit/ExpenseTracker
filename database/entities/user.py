from sqlalchemy import DATE, Column, Integer, String, TIMESTAMP, UUID, func
import uuid
from database.connect import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID, default=uuid.uuid4, unique=True, nullable=False)

    firstname = Column(String, index=True, nullable=False)
    lastname = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    birth = Column(DATE, nullable=True)

    created = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())