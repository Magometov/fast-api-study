from pydantic import BaseModel, Field, field_validator

from users.models import User, UserList

class Issue(BaseModel):
    title: str = Field(description='Название', max_length=20)
    assignee: User = Field(description='Исполнитель')