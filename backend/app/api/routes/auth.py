from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserCreate, UserRead
from app.services import auth_service
from app.services.audit_service import audit_service
from app.core.rate_limit import limiter
from app.services.user_service import get_user_by_email, get_user_by_username

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(
    request: Request,
    user_in: UserCreate,
    db: AsyncSession = Depends(deps.get_session)
):
    user = await auth_service.register_user(db, user_in=user_in)
    try:
        await audit_service.create_log(
            db,
            action="REGISTER",
            resource=f"user:{user.id}",
            user_id=user.id
        )
    except Exception as e:
        # Don't fail the request if audit logging fails
        print(f"Audit log failed: {e}")
    return user

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(
    request: Request,
    login_data: LoginRequest,
    db: AsyncSession = Depends(deps.get_session)
):
    token = await auth_service.authenticate_user(db, login_data=login_data)
    
    # Log login event - async and resilient
    try:
        user = await get_user_by_email(db, email=login_data.username_or_email)
        if not user:
            user = await get_user_by_username(db, username=login_data.username_or_email)
            
        if user:
            await audit_service.create_log(
                db,
                action="LOGIN",
                resource=f"user:{user.id}",
                user_id=user.id
            )
    except Exception as e:
        # Resilience: Don't block login if audit logging fails
        print(f"Audit log failed: {e}")
        
    return token

@router.get("/me", response_model=UserRead)
async def get_me(current_user=Depends(deps.get_current_user)):
    return current_user
