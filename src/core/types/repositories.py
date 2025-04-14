from sqlalchemy import inspect, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db.base import SAModel
from typing import Sequence

class BaseRepository[_MT: SAModel]:
    _model: type[_MT]

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> Sequence[_MT]:
        query = select(self._model)
        result = await self._session.execute(query)
        return result.scalars().all()

    @staticmethod
    def is_modified(instance: _MT) -> bool:
        inspr = inspect(instance)
        return inspr.modified or not inspr.has_identity

    async def save(self, instance: _MT) -> _MT:
        if not self.is_modified(instance):
            return instance

        self._session.add(instance)
        await self._session.flush()
        await self._session.refresh(instance)

        return instance
    
