from fastapi import status, HTTPException, APIRouter, Depends
from ..util import verify_password
# from ..models import UserDetail
from ..database import get_user_by_email
from ..oauth2 import *

router = APIRouter(prefix = "/login",tags = ['Authentication'])
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

@router.post("/")
def user_login(user_details: OAuth2PasswordRequestForm = Depends(), response_model = Token):
	user =  get_user_by_email(user_details.username)

	if not user:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Wrong Credentials!!!")
	if not verify_password(user_details.password, user.password):
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Wrong Credentials!!!")

	# Create JWT token
	token = create_access_token({"user_id":user.id})

	# Return token 
	return {"token": token, "token_type": "bearer"}	

