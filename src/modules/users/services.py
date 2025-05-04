from pytoniq import Address
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.models import User
from src.modules.users.repositories import UserRepository


async def _get_user_by_wallet(user_repo: UserRepository, wallet_address: str) -> User | None:
    return await user_repo.get_by_address(wallet_address)

async def _create_user(db_session: AsyncSession, wallet_address: str, user_repo: UserRepository) -> User:
    user = User(wallet_address=wallet_address)
    await user_repo.save(user)
    await db_session.commit()
    return user

async def get_or_create_user(db_session: AsyncSession, wallet_address: Address) -> User:
    user_repo = UserRepository(db_session)
    wallet_str = wallet_address.to_str()
    user = await _get_user_by_wallet(user_repo, wallet_str)
    if user is None:
        user = await _create_user(db_session, wallet_address, user_repo)
    return user
