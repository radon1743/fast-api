from fastapi import HTTPException
from sqlmodel import Field, SQLModel, Session, create_engine, select
from .models import *


sql_url = f"mysql+mysqlconnector://root@127.0.0.1:3306/instagram"

engine = create_engine(sql_url)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_all_post():
    with Session(engine) as session:
        statement = select(Post)
        results  = session.exec(statement)
        return results.all()  
    
def get_post_by_id(id: int):
    with Session(engine) as session:
        statment = select(Post).where(Post.id == id)
        result = session.exec(statment)
        return result.all()

def add_post(post: Post):
    with Session(engine) as session:
        session.add(post)
        session.commit()
        session.refresh(post)
        return post

def delete_by_id(id: int):
    with Session(engine) as session:
        post = session.get(Post, id)
        if not post:
            raise HTTPException(status_code=404,
                            detail=f"Post with this id = {id} not found")
        session.delete(post)
        session.commit()
        return 

def update_post_by_id(id: int, new_data: Post):
    with Session(engine) as session:
        post = session.get(Post, id)
        if not post:
            raise HTTPException(status_code=404,
                            detail=f"Post with this id = {id} not found")
        post.title = new_data.title
        post.content = new_data.content
        post.published = new_data.published
        session.add(post)
        session.commit()
        session.refresh(post)
