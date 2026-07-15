from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncIterator

from app.core.config import settings


engine = create_async_engine(settings.DATABASE_URL, echo=False)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncIterator[AsyncSession]:
    """
    Dependency для получения сессии БД.
    """

    async with AsyncSessionLocal() as session:
        yield session


async def close_db() -> None:
    """
    Корректно закрывает соединения с БД.
    """
    await engine.dispose()