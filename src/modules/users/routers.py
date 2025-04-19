import httpx
from fastapi import APIRouter, Depends, status
from typing import Annotated
from src.core.dependencies.db import get_async_session
from src.modules.users.dto import UserDTO, UserListDTO, UserCreateDTO, UserReadDTO
from src.modules.users.models import User
from src.modules.users.exceptions import UserException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence


from src.modules.users.repositories import UserRepository

UserRepoDep = Annotated[UserRepository, Depends(UserRepository)]

router = APIRouter(prefix='/users')

@router.post('/', response_model=UserReadDTO, responses={status.HTTP_201_CREATED: {'model': UserReadDTO}, status.HTTP_422_UNPROCESSABLE_ENTITY: {'model': UserException}}, status_code=status.HTTP_201_CREATED)
async def add_user_router(user: UserCreateDTO, db_session: AsyncSession = Depends(get_async_session)):
    async with db_session.begin():
        repo = UserRepository(db_session)
        convert_user = User(**user.model_dump())
        await repo.save(convert_user)
        return UserReadDTO.model_validate(convert_user)

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

@router.get('/balance/{wallet_id}')
async def get_wallet_balance(wallet_id: str):
    url = f"https://tonapi.io/v2/accounts/{wallet_id}"
    response = await httpx.AsyncClient().get(url)
    balance = response.json()['balance']
    result = balance / 1e9
    return result
