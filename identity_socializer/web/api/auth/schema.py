from pydantic import BaseModel

class SecurityToken(BaseModel):
    """
    Firebase-generated token.
    """
    token: str


class Success(BaseModel):
    """
    Yay.
    """
    msg: str
