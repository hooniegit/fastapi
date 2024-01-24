from fastapi import APIRouter # set router
from fastapi import Depends # set dependency
from fastapi import HTTPException # raise exception errors

from datetime import timedelta # (set/define) expire date
import os # file dir searching

from app.api.models.authenticaton import User, ClientCredentials

# set router
router = APIRouter()

# return client id & client secret to user
'''
curl -X 'POST' \
  'http://localhost:8000/key?username=<username>&password=<password>' \
  -H 'accept: application/json' \
  -d ''
'''
@router.post("/key")
async def return_keys(username:str, password:str):
    from app.api.lib.sqlite import fetchone_query

    DATABASE_FILE = f"{os.path.dirname(os.path.abspath(__file__))}/../sqlite/authentication.db"
    QUERY = "SELECT client_id, client_secret FROM user WHERE username = ? AND password = ?"
    VALUES = (username, password)
    result = fetchone_query(DATABASE_FILE, QUERY, VALUES)
    if result:
        return {"client_id": result[0], "client_secret": result[1]}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

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
from app.api.lib.authentication import create_access_token

@router.post("/token")
async def login_for_access_token(form_data: ClientCredentials):
    from app.api.lib.sqlite import fetchone_query
    
    DATABASE_FILE = f"{os.path.dirname(os.path.abspath(__file__))}/../sqlite/authentication.db"
    QUERY = f"SELECT username FROM user WHERE client_id = ? AND client_secret = ?"
    VALUES = (form_data.client_id, form_data.client_secret)
    username = fetchone_query(DATABASE_FILE, QUERY, VALUES)[0]
    
    # create access token
    if username:
        ACCESS_TOKEN_EXPIRE_MINUTES = 60
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username, "scope":form_data.scope}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    # raise exception error
    raise HTTPException(status_code=401, detail="Invalid credentials")

# return user infos
'''
curl \
  --request GET \
  --url 'localhost:8000/users/me' \
  --header 'Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJob29uaWVnaXQiLCJzY29wZSI6InN0cmluZyIsImV4cCI6MTcwNjExNjc4NX0.1PWlHmFEPFoN9fjml6wl-wfc36TrnXo9RAbppReAsHs'
'''
from app.api.dependencies.authentication import decode_access_token

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(decode_access_token)):
    return current_user
