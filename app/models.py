from typing import Optional
from sqlmodel import Field, ForeignKey, SQLModel
from pydantic import EmailStr



class Posts(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    published: bool = True
    user_id: int = Field(nullable=False,foreign_key="users.id", ondelete="CASCADE")    

class Users(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr =  Field(nullable=False, unique=True)
    password: str =  Field(nullable=False)
    
    
class UserCreate(SQLModel):
    email:EmailStr
    password:str

class UserRead(SQLModel):
    id:int
    email:EmailStr

class UserDetail(SQLModel):
    email:EmailStr
    password:str

class Token(SQLModel):
    token: str
    token_type: str

class TokenData(SQLModel):
    id: Optional[str] = None
