from fastapi import APIRouter, Depends, status
from typing import Annotated
from users.models import User
from users.exceptions import UserException

from users.repositories import UserRepository

UserRepoDep = Annotated[UserRepository, Depends(UserRepository)]

router = APIRouter(prefix='/users')

@router.post('/', responses={status.HTTP_201_CREATED: {'model': User}, status.HTTP_422_UNPROCESSABLE_ENTITY: {'model': UserException}}, status_code=status.HTTP_201_CREATED)
def add_user_router(user: User, repo: UserRepoDep):
    user = repo.create(user)
    return user

@router.get('/', responses={status.HTTP_200_OK: {'model': User}})
def get_users_router(repo: UserRepoDep):
    return repo.get_all()