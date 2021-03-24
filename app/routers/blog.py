from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..domain import schemas, database
from ..repository import blog_repository
from ..security import oauth2

router = APIRouter(
    prefix='/api/blogs',
    tags=['Blogs']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog)
async def add_blog(request: schemas.Blog,
                   db: Session = Depends(database.get_db),
                   current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = blog_repository.get_by_username(db, current_user.username)
    return blog_repository.create(db, request, user.id)


@router.get('/', response_model=List[schemas.ShowBlog])
async def get_blogs(db: Session = Depends(database.get_db)):
    return blog_repository.get_all(db)


@router.get('/mine', response_model=List[schemas.ShowBlog])
async def get_my_blogs(db: Session = Depends(database.get_db),
                       current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = blog_repository.get_by_username(db, current_user.username)
    return blog_repository.get_mine(db, user.id)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def get_blog(id: int, db: Session = Depends(database.get_db)):
    return blog_repository.get_by_id(db, id)


@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def remove_blog(id: int, db: Session = Depends(database.get_db),
                      current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = blog_repository.get_by_username(db, current_user.username)
    return blog_repository.delete_by_id(db, id, user.id)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update_blog(id: int, request: schemas.Blog, db: Session = Depends(database.get_db),
                      current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = blog_repository.get_by_username(db, current_user.username)
    return blog_repository.update(db, id, request, user.id)
