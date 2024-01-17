from fastapi import APIRouter # set router
from fastapi import Depends # set dependency
from fastapi import HTTPException, status # raise exception errors
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
    
# user model
class User:
    def __init__(self, username: str):
        self.username = username

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
@router.post("/key")
async def return_keys(username:str, password:str):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    query = f"SELECT client_id, client_secret FROM user WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    if result:
        return {"client_id": result[0], "client_secret": result[1]}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

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
'''
curl -X 'POST' \
  'http://localhost:8000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "client_id": "<client_id>",
  "client_secret": "<client_secret>"
}'
'''
@router.post("/token")
async def login_for_access_token(form_data: ClientCredentials):
    # define user information
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    query = f"SELECT username FROM user WHERE client_id = ? AND client_secret = ?"
    cursor.execute(query, (form_data.client_id, form_data.client_secret))
    username = cursor.fetchone()[0]
    conn.close()
    
    # create access token
    if username:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    # raise exception error
    raise HTTPException(status_code=401, detail="Invalid credentials")

# decode access token
def decode_auth(token: str):
    try:
        # decode token with secret key and algorithm
        decoded_credentials = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded_credentials["sub"]
        expire_date = decoded_credentials["exp"]
        
        return {"username": username, "expire_date": expire_date}
    
    # raise exception error
    except Exception as E:
        raise HTTPException(status_code=401, detail="Invalid authentication header")

def decode_access_token(token: str = Depends(oauth2_scheme)):
    # decode token & get infos
    user_info = decode_auth(token)
    username, expire_date = user_info["username"], user_info["expire_date"]

    # read information
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    query = "SELECT * FROM user WHERE username = ?"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    conn.close()

    # raise exception error (if credential invalid)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # raise exception error (if expired)
    expire_datetime = datetime.fromtimestamp(expire_date)
    if expire_datetime <= datetime.now():
        raise HTTPException(status_code=401, detail="Token expired")

    return username

# return user infos
'''
curl \
  --request GET \
  --url 'localhost:8000/users/me' \
  --header 'Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJob29uaWVnaXQiLCJleHAiOjE3MDU1MzMzMTR9.sO9CRQvWx7Pe7sm6inZVUCxWuKp_AtWD6rpcNvWwTwM'
'''
@router.get("/users/me")
async def read_users_me(current_user: User = Depends(decode_access_token)):
    return current_user
