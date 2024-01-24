from typing import Optional

def create_access_token(data: dict, expires_delta: Optional[int] = None):
    from app.api.lib.etc import read_configs
    from datetime import datetime, timedelta
    import jwt
    
    SECRET_KEY= read_configs("oauth", "SECRET_KEY")
    ALGORITHM= read_configs("oauth", "ALGORITHM")
    
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

def decode_auth(token: str):
    from app.api.lib.etc import read_configs
    from fastapi import HTTPException
    import jwt
    
    SECRET_KEY= read_configs("oauth", "SECRET_KEY")
    ALGORITHM= read_configs("oauth", "ALGORITHM")
    
    try:
        # decode token with secret key and algorithm
        decoded_credentials = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded_credentials["sub"]
        expire_date = decoded_credentials["exp"]
        scope = decoded_credentials["scope"]
        
        return {"username": username, "expire_date": expire_date, "scope": scope}
    
    # raise exception error
    except Exception as E:
        raise HTTPException(status_code=401, detail="Invalid authentication header")
    