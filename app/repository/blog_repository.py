from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..domain import schemas, models


def create(db: Session, request: schemas.BlogBase, author_id: int = 1):
    new_blog = models.Blog(title=request.title,
                           body=request.body, user_id=author_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def get_mine(db: Session, author_id: int):
    blogs = db.query(models.Blog).filter(
        models.Blog.user_id == author_id).all()
    return blogs


def get_by_id(db: Session, id: int):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog by id <{id}> was not found')
    return blog


def delete_by_id(db: Session, id: int, author_id=1):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog by id <{id}> was not found')
    # if_not_authorized(blog.first(), author_id)
    blog.delete(synchronize_session=False)
    db.commit()
    return 'deleted'


def if_not_authorized(blog, author_id):
    if not blog.user_id == author_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'Blog by id <{blog.id}> do not belong to you')


def update(db: Session, id: int, request: schemas.Blog, author_id=1):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog by id <{id}> was not found')
    # if_not_authorized(blog.first(), author_id)
    blog.update({models.Blog.title: request.title,
                 models.Blog.body: request.body}, synchronize_session=False)
    db.commit()
    return 'updated'


def get_by_username(db: Session, username: str):
    user = db.query(models.User).filter(
        models.User.username == username).first()
    if not user:
        pass
    user = db.query(models.User).filter(models.User.email == username).first()
    if not user:
        pass
    user = db.query(models.User).filter(models.User.cpf == username).first()
    if not user:
        pass
    user = db.query(models.User).filter(models.User.pis == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User by username <{username}> was not found')
    return user
