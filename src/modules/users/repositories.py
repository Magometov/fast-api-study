from sqlalchemy import select
from src.modules.users.models import User

from src.core.types.repositories import BaseRepository

class UserRepository(BaseRepository[User]):
    _model: type[User] = User

    async def get_by_id(self, id) -> User:
        query = select(self._model).where(self._model.id==id)
        result = await self._session.execute(query)
        return result.scalars().one()