from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserCreate
from app.services import user_service
from app.core.security import verify_password, create_access_token, create_refresh_token, verify_token
from app.models.user import User
import uuid

async def register_user(db: AsyncSession, user_in: UserCreate) -> User:
    user = await user_service.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    return await user_service.create_user(db, user_in=user_in)

async def authenticate_user(db: AsyncSession, login_data: LoginRequest) -> Token:
    # Try finding by email
    user = await user_service.get_user_by_email(db, email=login_data.username_or_email)
    
    # If not found by email, try finding by username
    if not user:
        user = await user_service.get_user_by_username(db, username=login_data.username_or_email)
        
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token = create_access_token(
        subject=user.id,
        role=user.role.value
    )
    refresh_token = create_refresh_token(
        subject=user.id
    )
    return Token(
        access_token=access_token, 
        refresh_token=refresh_token,
        token_type="bearer"
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
        
    access_token = create_access_token(
        subject=user.id,
        role=user.role.value
    )
    new_refresh_token = create_refresh_token(subject=user.id)
    
    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )
