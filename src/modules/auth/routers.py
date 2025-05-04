from typing import Annotated

from fastapi import APIRouter, Depends, status
from pytoniq import Address
from sqlalchemy.ext.asyncio import AsyncSession
from tonutils.tonconnect.utils.proof import generate_proof_payload

from src.core.api.exceptions.common import InternalServerErrorHTTPException
from src.core.dependencies.db import get_async_session
from src.modules.auth.constants import PROOF_TTL
from src.modules.auth.dto import JWTResponse, PayloadDTO, ProofVerificationDTO
from src.modules.auth.exceptions.application import ProofVerificationException
from src.modules.auth.exceptions.dto import ProofHTTPExceptionDTO
from src.modules.auth.exceptions.http import BaseProofHTTPException
from src.modules.auth.services.ton import check_proof
from src.modules.users.services import get_or_create_user
from src.modules.users.utils import JWT

router = APIRouter(prefix="/auth")


@router.get("/ton/", status_code=status.HTTP_200_OK)
def ton_proof_payload_generation() -> PayloadDTO:
    payload = generate_proof_payload(PROOF_TTL)
    return PayloadDTO(payload=payload)


@router.post(
    "/ton/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ProofHTTPExceptionDTO},
    },
)
async def ton_proof_verification(
    proof: ProofVerificationDTO,
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> JWTResponse:
    try:
        await check_proof(proof)
    except ProofVerificationException as exc:
        raise BaseProofHTTPException(detail=exc.message) from exc
    except Exception as exc:
        raise InternalServerErrorHTTPException from exc

    wallet_address = Address(proof.address)
    jwt_payload = {"wallet_id": wallet_address.to_str()}
    _ = await get_or_create_user(db_session, wallet_address)

    return JWT.create_tokens(data=jwt_payload)
