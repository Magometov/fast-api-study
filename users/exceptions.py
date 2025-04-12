from pydantic import BaseModel, RootModel

class UserAgeExceptionDetail(BaseModel):
    type: str = 'greater_than_equal'
    loc: list[str] = ["body", "age"]
    msg: str = 'Input should be greater than or equal to 18'
    input: int
    ctx: dict[str, int] = {'ge': 18}

class UserNameExceptionDetail(BaseModel):
    type: str = 'string_too_long'
    loc: list[str] = ["body", "name"]
    msg: str = 'String should have at most 20 characters'
    input: str
    ctx: dict[str, int] = {'max_length': 20}

class UserAgeException(BaseModel):
    detail: list[UserAgeExceptionDetail]

class UserNameException(BaseModel):
    detail: list[UserNameExceptionDetail]

class UserException(RootModel[UserAgeException | UserNameException]):...