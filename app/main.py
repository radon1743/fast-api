from contextlib import asynccontextmanager
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from .database import *
from .models import Posts,Users,UserCreate
from .util import *
from .routers import post,user,auth


@asynccontextmanager
async def insta_lifespan(app: FastAPI):
    create_db_and_table()
    yield


app = FastAPI(lifespan=insta_lifespan)

# def find_posts_index(id: int):
#     for i, post in enumerate(my_posts):
#         if post ["id"] == id:
#             return i
#     return None

@app.get("/")
def root():
    return {"message": "welcome to root page"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)






