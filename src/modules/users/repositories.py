from sqlalchemy import select

from src.core.types.repositories import BaseRepository
from src.modules.users.models import User


class UserRepository(BaseRepository[User]):
    _model: type[User] = User

    async def get_by_id(self, user_id: int) -> User | None:
        query = select(self._model).where(self._model.id == user_id)
        result = await self._session.execute(query)
        return result.scalars().one_or_none()

    async def get_by_address(self, address: str) -> User | None:
        query = select(self._model).where(self._model.wallet_address == address)
        result = await self._session.execute(query)
        return result.scalars().one_or_none()
