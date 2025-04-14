from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine, AsyncSession

from src.config import settings
from types import TracebackType

class AsyncSessionMaker:
    _engine: AsyncEngine = create_async_engine(url=settings.db.get_url().get_secret_value(), pool_pre_ping=True, future=True)
    _sessionmaker = async_sessionmaker(bind=_engine, autoflush=False, autocommit=False)

    def __init__(self) -> None:
        self._session = self._sessionmaker()

    async def __aenter__(self) -> AsyncSession:
        return await self._session.__aenter__()
    
    async def __aexit__[_BET: BaseException](self, type_: type[_BET], value: _BET, traceback: TracebackType) -> None:
        return await self._session.__aexit__(type_, value, traceback)