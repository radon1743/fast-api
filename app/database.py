from fastapi import HTTPException
from sqlmodel import Field, SQLModel, Session, create_engine, select
from .models import *
from pydantic import EmailStr



sql_url = f"mysql+mysqlconnector://rachit:mypassword@localhost:3306/rachit"

engine = create_engine(sql_url)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_all_post():
    with Session(engine) as session:
        statement = select(Posts)
        results  = session.exec(statement)
        return results.all()  
    
def get_post_by_id(id: int):
    with Session(engine) as session:
        statment = select(Posts).where(Post.id == id)
        result = session.exec(statment)
        return result.all()

def add_post(post: Posts):
    with Session(engine) as session:
        session.add(post)
        session.commit()
        session.refresh(post)
        return post

def delete_by_id(id: int):
    with Session(engine) as session:
        post = session.get(Posts, id)
        if not post:
            raise HTTPException(status_code=404,
                            detail=f"Post with this id = {id} not found")
        session.delete(post)
        session.commit()
        return 

def update_post_by_id(id: int, new_data: Posts):
    with Session(engine) as session:
        post = session.get(Posts, id)
        if not post:
            raise HTTPException(status_code=404,
                            detail=f"Post with this id = {id} not found")
        post.title = new_data.title
        post.content = new_data.content
        post.published = new_data.published
        session.add(post)
        session.commit()
        session.refresh(post)

def add_user(user: Users):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def get_user_by_id(id:int):
    with Session(engine) as session:
        statment = select(Users).where(Users.id == id)
        result = session.exec(statment)
        return result.first()

def get_user_by_email(email:EmailStr):
    with Session(engine) as session:
        statment = select(Users).where(Users.email == email)
        result = session.exec(statment)
        return result.first()



