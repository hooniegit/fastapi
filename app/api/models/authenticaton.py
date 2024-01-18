from pydantic import BaseModel

# usage: access token creation 
class ClientCredentials(BaseModel):
    client_id: str
    client_secret: str
    scope: str

# usage: return decoded informations
class User:
    def __init__(self, username: str, scope):
        self.username = username
        self.scope = scope
