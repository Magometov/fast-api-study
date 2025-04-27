from datetime import datetime
from typing import Annotated, Any

import pytoniq
from pydantic import BaseModel, ConfigDict, Field, RootModel, field_validator
from typing_extensions import Doc


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
    )


class UserDTO(BaseDTO):
    name: str = Field(description="Имя", max_length=20)
    age: int = Field(description="Возраст", ge=18, le=80)


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


class JWTPayload(BaseDTO):
    wallet_id: Annotated[str, Doc("Internal User Wallet ID")]
    exp: Annotated[datetime, Doc("Unix timestamp in seconds")]
    token_type: Annotated[str, Doc("Token type: access or refresh")]


class TokenRequest(BaseDTO):
    token: str


class JWTResponse(BaseDTO):
    access_token: str
    refresh_token: str


class WalletRequest(BaseDTO):
    wallet_id: str
