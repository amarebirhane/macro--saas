import uuid
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User
from app.schemas.user import UserAdminUpdate, UserCreate, UserUpdate
from app.utils.hashing import get_password_hash


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email, User.deleted_at == None)
    result = await db.execute(statement)
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
    statement = select(User).where(User.id == user_id, User.deleted_at == None)
    result = await db.execute(statement)
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    statement = select(User).where(User.username == username, User.deleted_at == None)
    result = await db.execute(statement)
    return result.scalars().first()


async def get_users_paginated(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> tuple[List[User], int]:
    # Get total count
    count_statement = select(func.count()).select_from(User).where(User.deleted_at == None)
    count_result = await db.execute(count_statement)
    total = count_result.scalar() or 0

    # Get paginated items
    statement = select(User).where(User.deleted_at == None).offset(skip).limit(limit)
    result = await db.execute(statement)
    items = result.scalars().all()

    return items, total


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    # Deprecated for paginated version but kept for compatibility if needed
    statement = select(User).where(User.deleted_at == None).offset(skip).limit(limit)
    result = await db.execute(statement)
    return result.scalars().all()


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    db_user = User(
        email=user_in.email,
        username=user_in.username,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, db_user: User, user_in: UserUpdate) -> User:
    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data:
        db_user.hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def admin_update_user(
    db: AsyncSession, db_user: User, user_in: UserAdminUpdate
) -> User:
    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data:
        db_user.hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, db_user: User) -> bool:
    from datetime import datetime
    db_user.deleted_at = datetime.utcnow()
    db.add(db_user)
    await db.commit()
    return True
