from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from config import ASYNC_DB_URL


Base = declarative_base()

async_engine = create_async_engine(ASYNC_DB_URL)

async_session = async_sessionmaker(bind=async_engine, class_=AsyncSession)

async def get_db():
    async with async_session() as session:
        yield session
