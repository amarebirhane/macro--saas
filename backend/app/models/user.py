import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from app.models.role import UserRole


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, nullable=False)
    username: Optional[str] = Field(default=None, unique=True, index=True)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    role: UserRole = Field(default=UserRole.USER, nullable=False)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)
    avatar_url: Optional[str] = Field(default=None, nullable=True)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False
    )
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
