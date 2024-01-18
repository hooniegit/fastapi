import jwt
from fastapi import HTTPException

# decode access token
def decode_auth(token: str):
    
    SECRET_KEY = "demo_authentication"
    ALGORITHM = "HS256"
    
    try:
        # decode token with secret key and algorithm
        decoded_credentials = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded_credentials["sub"]
        scope = decoded_credentials["scope"]
        expire_date = decoded_credentials["exp"]
        
        return {"username": username,
                "scope": scope,
                "expire_date": expire_date}
    
    # raise exception error
    except Exception as E:
        raise HTTPException(status_code=401, detail="Invalid authentication header")
    