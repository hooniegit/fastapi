from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from app.api.dependencies.authentication import get_current_user

router = APIRouter()


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import sqlite3
import jwt
from typing import Optional


SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DATABASE_FILE = "/Users/kimdohoon/git/study/python-fastapi/app/api/sqlite/user.db"
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

def create_access_token(data: dict, expires_delta: Optional[int] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    query = f"SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (form_data.username, form_data.password))
    user = cursor.fetchone()
    if user:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(oauth2_scheme)):
    return current_user
