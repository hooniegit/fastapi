from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.lib.authentication import decode_auth
from app.lib.sqlite import fetchone_query

from datetime import datetime
import os



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# depends with.. 
# - ClientCredentials(BaseModel)
def decode_access_token(token: str = Depends(oauth2_scheme)):
    # decode token & get infos
    user_info = decode_auth(token)
    username, scope, expire_date = user_info["username"][0], user_info["scope"], user_info["expire_date"]

    # return user
    dir = f"{os.path.dirname(os.path.abspath(__file__))}/../sqlite/authentication.db"
    QUERY = "SELECT * FROM user WHERE username = ?"
    user = fetchone_query(dir=dir, QUERY=QUERY, values=(username,))

    # raise exception error (if credential invalid)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # raise exception error (if expired)
    expire_datetime = datetime.fromtimestamp(expire_date)
    if expire_datetime <= datetime.now():
        raise HTTPException(status_code=401, detail="Token expired")

    return username, scope
