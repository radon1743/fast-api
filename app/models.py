from typing import Optional
from sqlmodel import Field, SQLModel


class Post(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    published: bool = True

class User(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str =  Field(nullable=False, unique=True)
    password: str =  Field(nullable=False)
    