from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..domain import schemas, database
from ..repository import user_repository, blog_repository
from ..security import oauth2

router = APIRouter(
    prefix='/api/users',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
async def add_user(request: schemas.CreateUser, db: Session = Depends(database.get_db)):
    return user_repository.create(db, request)


@router.get('/', response_model=List[schemas.ShowAuthor])
async def get_users(db: Session = Depends(database.get_db)):
    return user_repository.get_all(db)


# @router.get('/me', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
# async def get_me(db: Session = Depends(database.get_db),
#                  current_user: models.User = Depends(oauth2.get_current_user)):
#     user = blog_repository.get_by_username(db, current_user.username)
#     return user


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
async def get_user(id: int, db: Session = Depends(database.get_db)):
    return user_repository.get_by_id(db, id)


@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def remove_user(id: int, db: Session = Depends(database.get_db)):
    return user_repository.delete_by_id(db, id)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update_user(id: int, request: schemas.User, db: Session = Depends(database.get_db)):
    return user_repository.update(db, id, request)
