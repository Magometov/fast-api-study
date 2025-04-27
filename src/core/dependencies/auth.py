from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    InvalidSignatureError,
    PyJWTError,
)

from src.core.api.exceptions.common import AuthenticationHTTPException
from src.modules.users.dto import JWTPayload
from src.modules.users.utils import JWT

users_security = HTTPBearer(auto_error=False)


async def get_jwt_payload(creds: Annotated[HTTPAuthorizationCredentials | None, Depends(users_security)]) -> JWTPayload:
    if not creds:
        raise AuthenticationHTTPException(detail="Missing Authorization Credentials")
    try:
        return JWT.decode(token=creds.credentials)
    except ExpiredSignatureError as exc:
        raise AuthenticationHTTPException(detail="Expired JWT Credentials") from exc
    except (ValueError, DecodeError, InvalidSignatureError, PyJWTError) as exc:
        raise AuthenticationHTTPException(detail="Invalid token") from exc


JWTPayloadDep = Annotated[JWTPayload, Depends(get_jwt_payload)]
