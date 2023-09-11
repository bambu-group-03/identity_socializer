from pydantic import BaseModel

class SecurityToken(BaseModel):
    """
    Firebase-generated token.
    """
    token: str


class Signup(BaseModel):
    """
    Username, email and password for registration
    """
    username: str
    email: str
    password: str
