from typing import Any

import pytoniq
from pydantic import Field, RootModel, field_validator

from src.core.types.dto import BaseDTO


class UserDTO(BaseDTO):
    name: str | None = Field(description="Имя", max_length=20)
    age: int | None = Field(description="Возраст", ge=18, le=80)


class UserCreateDTO(UserDTO):
    wallet_address: str | None = Field(description="Адрес кошелька")

    @field_validator("wallet_address", mode="before")
    @classmethod
    def wallet_address_validate(cls, data: str | None) -> Any:
        if data is None:
            return None
        try:
            return pytoniq.Address(data).to_str()
        except Exception as e:
            msg = f"Error: {e}"
            raise ValueError(msg) from e


class UserReadDTO(BaseDTO):
    id: int = Field(description="id")
    name: str = Field(description="Имя", max_length=20)
    age: int = Field(description="Возраст", ge=18, le=80)
    wallet_address: str | None = Field(description="Адрес кошелька")


class UserListDTO(RootModel[list[UserDTO]]): ...


class TokenRequest(BaseDTO):
    token: str


class WalletRequest(BaseDTO):
    wallet_id: str
