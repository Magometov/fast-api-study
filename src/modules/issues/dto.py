from pydantic import BaseModel, Field

from src.modules.users.dto import UserDTO

class Issue(BaseModel):
    title: str = Field(description='Название', max_length=20)
    assignee: UserDTO = Field(description='Исполнитель')