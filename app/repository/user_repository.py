from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..domain import schemas, models, validation
from ..security import hashing


def create(db: Session, request: schemas.CreateUser):
    new_user = models.User(username=request.username,
                           email=request.email,
                           cpf=request.cpf,
                           pis=request.pis,
                           password=hashing.encrypt(request.password))

    verify_user(db, request)
    if not validation.validate_password(request.password, request.confirm):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Senha de confirmação e senha não batem! ")
    if not validation.validate_email(request.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"<{request.email}> não é um email válido!")
    if not validation.validate_cpf(request.cpf):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"\"{request.cpf}\" não é um CPF válido!")
    if not validation.validate_pis(request.pis):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"\"{request.pis}\" não é um PIS válido!")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all(db: Session):
    users = db.query(models.User).all()
    return users


def get_by_id(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User by id <{id}> was not found')
    return user


def verify_user(db: Session, request: schemas.User):
    user = db.query(models.User).filter(
        models.User.username == request.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Nome já em uso')

    user = db.query(models.User).filter(
        models.User.email == request.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Email já em uso')

    user = db.query(models.User).filter(models.User.cpf == request.cpf).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='CPF já em uso')

    user = db.query(models.User).filter(models.User.pis == request.pis).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='PIS já em uso')
    return user


def delete_by_id(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id)
    user_blogs = db.query(models.Blog).filter(models.Blog.user_id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User by id <{id}> was not found')

    if user_blogs:
        user_blogs.delete(synchronize_session=False)

    user.delete(synchronize_session=False)
    db.commit()
    return 'deleted'


def update(db: Session, id: int, request: schemas.User):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog by id <{id}> was not found')

    user.update({models.User.username: request.username,
                 models.User.email: request.email,
                 models.User.cpf: request.cpf,
                 models.User.pis: request.pis,
                 models.User.password: hashing.encrypt(request.password)}, synchronize_session=False)
    db.commit()
    return 'updated'
