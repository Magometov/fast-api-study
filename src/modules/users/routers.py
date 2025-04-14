from fastapi import APIRouter, Depends, status
from typing import Annotated
from src.core.dependencies.db import get_async_session
from src.modules.users.dto import UserDTO, UserListDTO
from src.modules.users.models import User
from src.modules.users.exceptions import UserException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence


from src.modules.users.repositories import UserRepository

UserRepoDep = Annotated[UserRepository, Depends(UserRepository)]

router = APIRouter(prefix='/users')

@router.post('/', responses={status.HTTP_201_CREATED: {'model': UserDTO}, status.HTTP_422_UNPROCESSABLE_ENTITY: {'model': UserException}}, status_code=status.HTTP_201_CREATED)
async def add_user_router(user: UserDTO, db_session: AsyncSession = Depends(get_async_session)):
    repo = UserRepository(db_session)
    convert_user = User(**user.model_dump())
    await repo.save(convert_user)
    await db_session.commit()
    return user

@router.get('/', response_model=UserListDTO)
async def get_users_router(db_session: AsyncSession = Depends(get_async_session)) -> Sequence[User]:
    repo = UserRepository(db_session)
    users = await repo.get_all()
    return users

@router.get('/{id}', response_model=UserDTO)
async def get_user_router(id: int, db_session: AsyncSession = Depends(get_async_session)) -> User:
    repo = UserRepository(db_session)
    user = await repo.get_by_id(id)
    return user
