from fastapi import APIRouter # set router
from fastapi import Depends # set dependency
from fastapi import HTTPException # raise exception errors
from fastapi.security import OAuth2PasswordBearer # create scheme

import jwt # decode token with params
from pydantic import BaseModel # create cliend credential model
from datetime import datetime, timedelta # (set/define) expire date
import sqlite3 # read database
import os # file dir searching
from typing import Optional # set optional variables

# cliend credential model
class ClientCredentials(BaseModel):
    client_id: str
    client_secret: str
    scope: str
    
# set router
router = APIRouter()

# token
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# sqlite database dir
DATABASE_FILE = f"{os.path.dirname(os.path.abspath(__file__))}/../sqlite/authentication.db"

# create scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# return client id & client secret to user
'''
curl -X 'POST' \
  'http://localhost:8000/key?username=<username>&password=<password>' \
  -H 'accept: application/json' \
  -d ''
'''
@router.get("/key")
async def return_keys(username:str, password:str):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    query = f"SELECT client_id, client_secret FROM user WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    if result:
        return {"client_id": result[0], "client_secret": result[1]}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

# create access token
def create_access_token(data: dict, expires_delta: Optional[int] = None):
    # copy data
    to_encode = data.copy()
    
    # set expire date(timestamp)
    if expires_delta:
        expire = datetime.now() + expires_delta
        to_encode.update({"exp": expire})
    else:
        expire = datetime.now() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
    
    # encode data == create access token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

# create & return access token
@router.post("/token")
async def return_access_token(form_data: ClientCredentials = Depends(create_access_token)):
    # define user information
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    query = f"SELECT username FROM user WHERE client_id = ? AND client_secret = ?"
    cursor.execute(query, (form_data.client_id, form_data.client_secret))
    username = cursor.fetchone()
    print(username)
    conn.close()
    
    # create access token
    if username:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"username": username, "scope": form_data.scope}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    # raise exception error
    raise HTTPException(status_code=401, detail="Invalid credentials")

# decode access token

# return user infos
'''
curl \
  --request GET \
  --url 'localhost:8000/users/me' \
  --header 'Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6WyJob29uaWVnaXQiXSwic2NvcGUiOiJERU1PIiwiZXhwIjoxNzA1NjI1NTcwfQ.RR4cEaQpKw09gZsXzcbQRgieEmSBDsWjPtbh0zG4ALA'
'''

from app.api.dependencies.authentication import decode_access_token
from app.api.models.authenticaton import User

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(decode_access_token)):
    return current_user
