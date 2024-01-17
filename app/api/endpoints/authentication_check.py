from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import sqlite3
import jwt
import os
from typing import Optional

# set router
router = APIRouter()

# token
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# sqlite database dir
DATABASE_FILE = f"{os.path.dirname(os.path.abspath(__file__))}/../sqlite/user.db"

# create scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# create user
class User:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

def create_access_token(data: dict, expires_delta: Optional[int] = None):
    # copy data
    to_encode = data.copy()
    
    # set expire date(timestamp)
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    
    # encode data == create access token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # define user information
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (form_data.username, form_data.password))
    user = cursor.fetchone()
    conn.close()
    
    # create access token
    if user:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    # 
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
def decode_auth(token: str):
    try:
        # decode token with secret key and algorithm
        decoded_credentials = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded_credentials["sub"]
        expire_date = decoded_credentials["exp"]
        
        return {"username": username, "expire_date": expire_date}
    
    except Exception as E:
        raise HTTPException(status_code=401, detail="Invalid authentication header") from E

def oauth2_scheme(token: str = Depends(oauth2_scheme)):
    # decode token & get infos
    user_info = decode_auth(token)
    username, expire_date = user_info["username"], user_info["expire_date"]

    # read information
    print(">>>>>>> " + username + str(expire_date)) # <---- TEST
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    expire_datetime = datetime.fromtimestamp(expire_date)
    if expire_datetime >= datetime.now():
        print("TOKEN EXPIRED")
        raise HTTPException(status_code=401, detail="TOKEN EXPIRED")
        
    print("USER EXISTS")

    return username


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(oauth2_scheme)):
    return current_user

# curl \
#   --request GET \
#   --url 'localhost:8000/users/me' \
#   --header 'Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJob29uaWVnaXQiLCJleHAiOjE3MDU1MjEwNzZ9.dbFSlNeO3ujPrPjMGd2haccnNFAjXocrgTbrH3waS2w'