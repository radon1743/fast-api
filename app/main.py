from contextlib import asynccontextmanager
from random import randrange
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from .database import *
from .models import Post

@asynccontextmanager
async def insta_lifespan(app: FastAPI):
    create_db_and_table()
    yield


app = FastAPI(lifespan=insta_lifespan)

my_posts = [{},{}]


# def get_posts_by_id(id: int) -> Post:
#     for i in my_posts:
#         if i["id"] == id:
#             return i
#     return None

def find_posts_index(id: int):
    for i, post in enumerate(my_posts):
        if post ["id"] == id:
            return i
    return None


@app.get("/")
def root():
    return {"message": "welcome to root page"}

@app.get("/posts")
def get_posts():
    post_dict = get_all_post()
    # print(post_dict)
    return {"data":post_dict}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def save_posts(post: Post):
    post_dict = add_post(post)
    return post_dict

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post =  get_post_by_id(id)
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with this id = {id} not found")
    return post

@app.delete("/posts/{id}")
def delete_post(id: int, status_code = status.HTTP_204_NO_CONTENT) :
    delete_by_id(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    update_post_by_id(id, post)
    
    return {"message": f"Updated post with id {id}"}

