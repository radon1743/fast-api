from fastapi import Body, FastAPI, Response, status, HTTPException, APIRouter
from ..database import *
from ..models import Posts,Users,UserCreate
from ..util import *


router = APIRouter(prefix = "/users", tags = ['User'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = UserRead)
def create_user(user:UserCreate):

    # Hash password 
    user.password = hash(user.password)

    new_user = Users(**user.dict())
    new_user = add_user(new_user)
    return new_user


@router.get("/{id}")
def get_user(id:int):

    user = get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with this id = {id} not found")
    return UserRead(**user.dict())
