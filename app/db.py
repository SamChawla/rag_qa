""" Database configuration and session management """

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()

async def get_session() -> AsyncSession:
    """ Get an async session from the sessionmaker """
    async with async_session() as session:
        yield session