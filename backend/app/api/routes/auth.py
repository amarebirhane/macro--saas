from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core.rate_limit import limiter
from app.schemas.auth import (
    LoginRequest,
    PasswordResetConfirm,
    PasswordResetRequest,
    RefreshTokenRequest,
    Token,
)

# ... (rest of imports)

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


@router.get("/me", response_model=UserRead)
async def get_me(current_user=Depends(deps.get_current_user)):
    return current_user
