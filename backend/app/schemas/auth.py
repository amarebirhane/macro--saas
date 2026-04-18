from pydantic import BaseModel
from typing import Optional
from app.models.role import UserRole

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None

class LoginRequest(BaseModel):
    username_or_email: str
    password: str
