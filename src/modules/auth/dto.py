from datetime import datetime
from typing import Annotated

from pydantic import Field
from typing_extensions import Doc

from src.core.types.dto import BaseDTO


class PayloadDTO(BaseDTO):
    payload: str


class Domain(BaseDTO):
    length_bytes: int = Field(alias="lengthBytes")
    value: str


class ProofDTO(BaseDTO):
    timestamp: int
    domain: Domain
    payload: str
    signature: str
    state_init: str


class ProofVerificationDTO(BaseDTO):
    address: str
    network: int
    proof: ProofDTO


class JWTResponse(BaseDTO):
    access_token: str
    refresh_token: str


class JWTPayload(BaseDTO):
    wallet_id: Annotated[str, Doc("Internal User Wallet ID")]
    exp: Annotated[datetime, Doc("Unix timestamp in seconds")]
    token_type: Annotated[str, Doc("Token type: access or refresh")]
