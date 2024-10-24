from pydantic import BaseModel


class Token(BaseModel):
  access_token: str
  token_type:str

class TokenData(BaseModel):
    username:str | None = None
    phone_number:str | None = None