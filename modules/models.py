from pydantic import BaseModel, EmailStr
from typing import Optional


class Regist(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    passwd: Optional[str]

class GettingTokens(BaseModel):
    access_token: str
    refresh_token: str

class RefreshModel(BaseModel):
    email: Optional[EmailStr]
    refresh_token: Optional[str]