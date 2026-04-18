from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core.rate_limit import limiter
from app.models.user import User
from app.schemas.auth import (
    ChangePasswordRequest,
    LoginRequest,
    PasswordResetConfirm,
    RefreshTokenRequest,
    Token,
)
from app.schemas.user import UserCreate, UserRead
from app.services import auth_service
from app.services.audit_service import audit_service
from app.services.user_service import get_user_by_email, get_user_by_username

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(
    request: Request, user_in: UserCreate, db: AsyncSession = Depends(deps.get_session)
):
    user = await auth_service.register_user(db, user_in=user_in)
    try:
        await audit_service.create_log(
            db, action="REGISTER", resource=f"user:{user.id}", user_id=user.id
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
    db: AsyncSession = Depends(deps.get_session),
):
    token = await auth_service.authenticate_user(db, login_data=login_data)

    # Log login event - async and resilient
    try:
        user = await get_user_by_email(db, email=login_data.username_or_email)
        if not user:
            user = await get_user_by_username(db, username=login_data.username_or_email)

        if user:
            await audit_service.create_log(
                db, action="LOGIN", resource=f"user:{user.id}", user_id=user.id
            )
    except Exception as e:
        # Resilience: Don't block login if audit logging fails
        print(f"Audit log failed: {e}")

    return token


@router.post("/refresh", response_model=Token)
@limiter.limit("10/minute")
async def refresh_token(
    request: Request,
    token_data: RefreshTokenRequest,
    db: AsyncSession = Depends(deps.get_session),
):
    """
    Refresh access token using a valid refresh token.
    """
    return await auth_service.refresh_access_token(
        db, refresh_token=token_data.refresh_token
    )


@router.post("/verify-email", status_code=status.HTTP_200_OK)
async def verify_email(
    token: str,
    db: AsyncSession = Depends(deps.get_session),
):
    """
    Verify a user's email address using the token sent via email.
    """
    await auth_service.verify_email_token(db, token=token)
    return {"message": "Email verified successfully"}


@router.post("/password-recovery/{email}", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")
async def recover_password(
    request: Request,
    email: str,
    db: AsyncSession = Depends(deps.get_session),
):
    """
    Password recovery endpoint to send a reset link.
    """
    await auth_service.request_password_reset(db, email=email)
    return {"message": "Password recovery email sent"}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    reset_data: PasswordResetConfirm,
    db: AsyncSession = Depends(deps.get_session),
):
    """
    Reset password using a valid reset token.
    """
    await auth_service.reset_password(
        db, token=reset_data.token, new_password=reset_data.new_password
    )
    return {"message": "Password reset successfully"}


@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_session),
):
    """
    Change password for the currently authenticated user.
    """
    await auth_service.change_password(
        db, user=current_user, old_password=data.old_password, new_password=data.new_password
    )
    return {"message": "Password changed successfully"}


@router.post("/test-email", status_code=status.HTTP_200_OK, tags=["Testing"])
async def test_email(
    email: str,
):
    """
    Diagnostic endpoint to send a test welcome email using the background worker.
    """
    from app.core.redis import get_arq_pool
    arq_pool = await get_arq_pool()
    await arq_pool.enqueue_job(
        "send_welcome_email_task",
        email=email,
        name="Test User"
    )
    return {"message": f"Test email queued for {email}. Check your console/worker logs!"}


@router.get("/me", response_model=UserRead)
async def get_me(current_user=Depends(deps.get_current_user)):
    return current_user
