from fastapi import Body, Depends, FastAPI, Response, status, HTTPException, APIRouter

from app import oauth2
from ..database import *
from ..models import Posts,Users,UserCreate
# from ..util import *


router = APIRouter( prefix = "/posts", tags = ['Post'])


@router.get("/")  
def get_posts():
    post_dict = get_all_post()
    # print(post_dict)
    return {"data":post_dict}


@router.post("/", status_code=status.HTTP_201_CREATED)
def save_posts(post: Posts, user_id = Depends(oauth2.get_current_user)  ):
    print(user_id)
    post_dict = add_post(post)
    return post_dict

@router.get("/{id}")
def get_post(id: int, response: Response):
    post =  get_post_by_id(id)
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with this id = {id} not found")
    return post

@router.delete("/{id}")
def delete_post(id: int, 
                status_code = status.HTTP_204_NO_CONTENT, 
                user_id = Depends(oauth2.get_current_user) ) :
    delete_by_id(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id: int,
                post: Posts, 
                user_id = Depends(oauth2.get_current_user) ):
    update_post_by_id(id, post)
    
    return {"message": f"Updated post with id {id}"}
