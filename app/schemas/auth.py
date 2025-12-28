from pydantic import BaseModel


class Token(BaseModel):
    """
    represents an authentication token returned after a successful login.
    """

    access_token: str
    token_type: str
