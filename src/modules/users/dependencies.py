from typing import Annotated

from fastapi import Depends

from src.core.dependencies.auth import JWTPayloadDep

__all__ = ("CurrentWalletIDDep", "get_current_wallet_id")


async def get_current_wallet_id(jwt_payload: JWTPayloadDep) -> str:
    return jwt_payload.wallet_id


CurrentWalletIDDep = Annotated[int, Depends(get_current_wallet_id)]
