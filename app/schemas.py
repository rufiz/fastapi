from typing import Optional
from pydantic import BaseModel, EmailStr

from datetime import date, datetime

from pydantic.types import conint

from app.database import Base


class User(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class ResponseUser(BaseModel):
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut


class PostOut(BaseModel):
    Post: Post
    votes: int


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
