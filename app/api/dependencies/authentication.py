from fastapi import Depends # set dependency
from fastapi.security import OAuth2PasswordBearer # create scheme
from fastapi import HTTPException

# create scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def decode_access_token(token: str = Depends(oauth2_scheme)):
    from app.api.lib.authentication import decode_auth
    from app.api.lib.sqlite import fetchone_query
    from datetime import datetime
    import os
 
    # decode token & get infos
    user_info = decode_auth(token)
    username, expire_date, scope = user_info["username"], user_info["expire_date"], user_info["scope"]

    # read information
    DATABASE_FILE = f"{os.path.dirname(os.path.abspath(__file__))}/../sqlite/authentication.db"
    QUERY = "SELECT * FROM user WHERE username = ?"
    VALUES = (username,)
    user = fetchone_query(DATABASE_FILE, QUERY, VALUES)

    # raise exception error (if credential invalid)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # raise exception error (if expired)
    expire_datetime = datetime.fromtimestamp(expire_date)
    if expire_datetime <= datetime.now():
        raise HTTPException(status_code=401, detail="Token expired")

    return username, scope