from pydantic import BaseModel, Field, RootModel

from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
    )

class UserDTO(BaseDTO):
    name: str = Field(description='Имя', max_length=20)
    age: int = Field(description='Возраст', ge=18, le=80)

class UserListDTO(RootModel[list[UserDTO]]):...