from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid
from app.models.role import UserRole

class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Optional[UserRole] = UserRole.USER

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserAdminUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
