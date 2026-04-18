from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid
from app.models.role import UserRole

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, nullable=False)
    role: UserRole = Field(default=UserRole.USER, nullable=False)
    is_active: bool = Field(default=True)

class User(UserBase, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False
    )
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

class UserCreate(UserBase):
    password: str

class UserUpdate(SQLModel):
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
