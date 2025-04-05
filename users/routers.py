from fastapi import APIRouter, Depends
from typing import Annotated
from users.models import User

from users.repositories import UserRepository

UserRepoDep = Annotated[UserRepository, Depends(UserRepository)]

router = APIRouter(prefix='/users')

@router.post('/')
def add_user_router(user: User, repo: UserRepoDep):
    user = repo.create(user)
    return user

@router.get('/')
def get_users_router(repo: UserRepoDep):
    return repo.get_all()