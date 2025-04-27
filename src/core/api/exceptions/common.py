from fastapi import status

from src.core.api.exceptions.base import BaseHTTPException


class AuthenticationHTTPException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Authentication credentials were not provided"
