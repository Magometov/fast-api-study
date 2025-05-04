from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from fastapi import HTTPException

from src.config import settings
from src.modules.auth.dto import JWTPayload, JWTResponse
from src.modules.users.constants import REFRESH_TOKEN_TYPE


class JWT:
    _access_token_expire_delta = timedelta(minutes=settings.jwt.access_token_expire_minutes)
    _refresh_token_expire_delta = timedelta(days=settings.jwt.refresh_token_expire_days)
    _secret_key = settings.jwt.secret_key

    @classmethod
    def decode(cls, token: str) -> JWTPayload:
        payload = jwt.decode(token, cls._secret_key, algorithms=[settings.jwt.algorithm])
        return JWTPayload.model_validate(payload)

    @classmethod
    def create_access_token(cls, data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
        expires_delta = expires_delta or cls._access_token_expire_delta
        expire = datetime.now(UTC) + expires_delta
        to_encode = JWTPayload.model_validate({**data, "exp": expire, "token_type": "access"})
        return jwt.encode(to_encode.model_dump(), cls._secret_key, algorithm=settings.jwt.algorithm)

    @classmethod
    def create_refresh_token(cls, data: dict[str, Any]) -> str:
        expire = datetime.now(UTC) + cls._refresh_token_expire_delta
        to_encode = JWTPayload.model_validate({**data, "exp": expire, "token_type": "refresh"})
        return jwt.encode(to_encode.model_dump(), cls._secret_key, algorithm=settings.jwt.algorithm)

    @classmethod
    def create_tokens(cls, data: dict[str, Any]) -> JWTResponse:
        access_token = cls.create_access_token(data)
        refresh_token = cls.create_refresh_token(data)
        return JWTResponse(access_token=access_token, refresh_token=refresh_token)

    @classmethod
    def update_tokens(cls, token: str) -> JWTResponse:
        try:
            payload = cls.decode(token)
            if payload.token_type != REFRESH_TOKEN_TYPE:
                raise HTTPException(status_code=401, detail="Invalid token type") from None
        except jwt.ExpiredSignatureError as err:
            raise HTTPException(status_code=401, detail="Token has expired") from err
        except jwt.DecodeError as err:
            raise HTTPException(status_code=401, detail="Token is invalid") from err
        return cls.create_tokens(data={"wallet_id": payload.wallet_id})
