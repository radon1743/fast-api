from jose import ExpiredSignatureError, JWTError, jwt
from datetime import datetime, timedelta, timezone
from .models import Token, TokenData
from fastapi.security import OAuth2PasswordBearer 
from fastapi import HTTPException, Depends, status

oauth2_schema = OAuth2PasswordBearer(tokenUrl ='login')

# SECRET KEY
# ALGORITH
# EXPIRAITON TIME 

SECRET_KEY = "This is a secret key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 30  

def create_access_token(data:dict):
	to_encode = data.copy()

	expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_TIME)
	to_encode.update({"exp":expire})

	encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

	return encoded_token

def verify_token(token:str, credentials_exception):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		id:str =  payload.get("user_id")
		if not id:
			raise credentials_exception
		token_data = TokenData(id=str(id))
	except ExpiredSignatureError:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
	except JWTError:
		raise credentials_exception
	return token_data

def get_current_user(token:str = Depends(oauth2_schema)):
	credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
									   detail= "Not valid details",
									   headers={"WWW-Authenticate":  "Bearer"})
	return verify_token(token, credentials_exception)


