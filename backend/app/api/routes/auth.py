from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserCreate, UserRead
from app.services import auth_service
from app.core.rate_limit import limiter

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(
    request: Request,
    user_in: UserCreate,
    db: AsyncSession = Depends(deps.get_session)
):
    return await auth_service.register_user(db, user_in=user_in)

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(
    request: Request,
    login_data: LoginRequest,
    db: AsyncSession = Depends(deps.get_session)
):
    return await auth_service.authenticate_user(db, login_data=login_data)

@router.get("/me", response_model=UserRead)
async def get_me(current_user=Depends(deps.get_current_user)):
    return current_user
