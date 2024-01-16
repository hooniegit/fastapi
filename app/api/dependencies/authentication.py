from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

class User:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    if token != "fake-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return User(username="john_doe", email="john@example.com")
