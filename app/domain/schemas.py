from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    cpf: str
    pis: str
    password: str


class User(UserBase):
    class Config():
        orm_mode = True


class CreateUser(BaseModel):
    username: str
    email: str
    cpf: str
    pis: str
    password: str
    confirm: str

    class Config():
        orm_mode = True


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    class Config():
        orm_mode = True


class ShowUser(BaseModel):
    username: str
    email: str
    cpf: str
    pis: str
    blogs: List[Blog] = []

    class Config():
        orm_mode = True


class ShowAuthor(BaseModel):
    username: str
    email: str
    cpf: str
    pis: str

    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    author: ShowAuthor

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
