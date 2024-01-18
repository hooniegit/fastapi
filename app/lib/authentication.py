import jwt
from fastapi import HTTPException
from typing import Optional # set optional variables
from datetime import datetime, timedelta

def create_access_token(data: dict, expires_delta: Optional[int] = None):
    
    SECRET_KEY = "mysecretkey"
    ALGORITHM = "HS256"
    
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

# decode access token
def decode_access_token(token: str):
    
    SECRET_KEY = "mysecretkey"
    ALGORITHM = "HS256"
    
    try:
        # decode token with secret key and algorithm
        decoded_credentials = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded_credentials["username"]
        scope = decoded_credentials["scope"]
        expire_date = decoded_credentials["exp"]
        
        return {"username": username,
                "scope": scope,
                "expire_date": expire_date}
    
    # raise exception error
    except Exception as E:
        raise HTTPException(status_code=401, detail="Invalid authentication header")

