import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.redis import get_arq_pool
from app.core.security import (
    create_access_token,
    create_password_reset_token,
    create_refresh_token,
    create_verification_token,
    verify_token,
)
from app.models.user import User
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserCreate
from app.services import user_service
from app.utils.hashing import get_password_hash, verify_password


async def register_user(db: AsyncSession, user_in: UserCreate) -> User:
    user = await user_service.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    new_user = await user_service.create_user(db, user_in=user_in)

    # Queue welcome and verification emails
    try:
        arq_pool = await get_arq_pool()
        await arq_pool.enqueue_job(
            "send_welcome_email_task",
            email=new_user.email,
            name=f"{new_user.first_name or ''} {new_user.last_name or ''}".strip() or new_user.username
        )

        verify_token_str = create_verification_token(subject=new_user.id)
        verify_link = f"{settings.FRONTEND_URL}/verify-email?token={verify_token_str}"
        await arq_pool.enqueue_job(
            "send_verification_email_task",
            email=new_user.email,
            name=new_user.first_name or new_user.username,
            link=verify_link
        )
    except Exception as e:
        # Don't fail registration if email queuing fails, but log it
        print(f"Failed to queue emails for user {new_user.email}: {e}")

    return new_user


async def verify_email_token(db: AsyncSession, token: str) -> bool:
    payload = verify_token(token, token_type="verification")
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")

    user_id = payload.get("sub")
    user = await user_service.get_user_by_id(db, user_id=uuid.UUID(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    db.add(user)
    await db.commit()
    return True


async def request_password_reset(db: AsyncSession, email: str) -> bool:
    user = await user_service.get_user_by_email(db, email=email)
    if not user:
        # For security, we don't reveal if the user exists
        return True

    reset_token = create_password_reset_token(subject=user.id)
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

    try:
        arq_pool = await get_arq_pool()
        await arq_pool.enqueue_job(
            "send_password_reset_email_task",
            email=user.email,
            name=user.first_name or user.username,
            link=reset_link
        )
    except Exception as e:
        print(f"Failed to queue password reset email for {email}: {e}")
        return False

    return True


async def reset_password(db: AsyncSession, token: str, new_password: str) -> bool:
    payload = verify_token(token, token_type="reset")
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    user_id = payload.get("sub")
    user = await user_service.get_user_by_id(db, user_id=uuid.UUID(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = get_password_hash(new_password)
    db.add(user)
    await db.commit()
    return True


async def change_password(db: AsyncSession, user: User, old_password: str, new_password: str) -> bool:
    if not verify_password(old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    
    user.hashed_password = get_password_hash(new_password)
    db.add(user)
    await db.commit()
    return True


async def authenticate_user(db: AsyncSession, login_data: LoginRequest) -> Token:
    # Try finding by email
    user = await user_service.get_user_by_email(db, email=login_data.username_or_email)

    # If not found by email, try finding by username
    if not user:
        user = await user_service.get_user_by_username(
            db, username=login_data.username_or_email
        )

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token = create_access_token(subject=user.id, role=user.role.value)
    refresh_token = create_refresh_token(subject=user.id)
    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


async def refresh_access_token(db: AsyncSession, refresh_token: str) -> Token:
    payload = verify_token(refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = await user_service.get_user_by_id(db, user_id=uuid.UUID(user_id))
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    access_token = create_access_token(subject=user.id, role=user.role.value)
    new_refresh_token = create_refresh_token(subject=user.id)

    return Token(
        access_token=access_token, refresh_token=new_refresh_token, token_type="bearer"
    )
