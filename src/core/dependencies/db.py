from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.sessions import AsyncSessionMaker

__all__ = ("get_async_session",)


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionMaker() as session:
        yield session
