from pydantic import BaseModel, Field, RootModel, ConfigDict, field_validator

import pytoniq


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
    )

class UserDTO(BaseDTO):
    name: str = Field(description='Имя', max_length=20)
    age: int = Field(description='Возраст', ge=18, le=80)

class UserCreateDTO(UserDTO):
    wallet_address: str | None = Field(description='Адрес кошелька')

    @field_validator('wallet_address', mode='before')
    @classmethod
    def wallet_address_validate(cls, data: str|None) -> str|None:
        if data is None:
            return None
        try:
            return pytoniq.Address(data).to_str()
        except Exception as e:
            raise ValueError(f"Error: {e}")

class UserReadDTO(BaseDTO):
    id: int = Field(description='id')
    name: str = Field(description='Имя', max_length=20)
    age: int = Field(description='Возраст', ge=18, le=80)
    wallet_address: str | None = Field(description='Адрес кошелька')

class UserListDTO(RootModel[list[UserDTO]]):...