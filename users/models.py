from pydantic import BaseModel, Field, RootModel

class User(BaseModel):
    name: str = Field(description='Имя', max_length=20)
    age: int = Field(description='Возраст', ge=18, le=80)

class UserList(RootModel[list[User]]):...