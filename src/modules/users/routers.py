from collections.abc import Sequence
from typing import Annotated, Any

import httpx
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies.db import get_async_session
from src.modules.users.dependencies import CurrentWalletIDDep
from src.modules.users.dto import (
    JWTResponse,
    TokenRequest,
    UserCreateDTO,
    UserDTO,
    UserListDTO,
    UserReadDTO,
    WalletRequest,
)
from src.modules.users.exceptions import UserException
from src.modules.users.models import User
from src.modules.users.repositories import UserRepository
from src.modules.users.utils import JWT

UserRepoDep = Annotated[UserRepository, Depends(UserRepository)]
AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]

router = APIRouter(prefix="/users")


@router.post(
    "/",
    responses={
        status.HTTP_201_CREATED: {"model": UserReadDTO},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": UserException},
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_user_router(user: UserCreateDTO, db_session: AsyncSessionDep) -> UserReadDTO:
    async with db_session.begin():
        repo = UserRepository(db_session)
        convert_user = User(**user.model_dump())
        await repo.save(convert_user)
        return UserReadDTO.model_validate(convert_user)


@router.get("/", response_model=UserListDTO)
async def get_users_router(db_session: AsyncSessionDep) -> Sequence[User]:
    repo = UserRepository(db_session)
    return await repo.get_all()


@router.get("/{user_id}", response_model=UserDTO)
async def get_user_router(user_id: int, db_session: AsyncSessionDep) -> User:
    repo = UserRepository(db_session)
    return await repo.get_by_id(user_id)


@router.get("/wallet_balance/")
async def get_wallet_balance(wallet_id: CurrentWalletIDDep) -> Any:
    url = f"https://tonapi.io/v2/accounts/{wallet_id}"
    response = await httpx.AsyncClient().get(url)
    balance = response.json()["balance"]
    return balance / 1e9


@router.post("/tokens/")
async def get_tokens(wallet: WalletRequest) -> JWTResponse:
    return JWT.create_tokens({"wallet_id": wallet.wallet_id})


@router.post("/update_tokens/")
async def update_tokens(data: TokenRequest) -> JWTResponse:
    return JWT.update_tokens(data.token)
