import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.role import UserRole
from app.schemas.user import UserAdminUpdate, UserRead
from app.services import user_service

router = APIRouter()


@router.get("/users", response_model=List[UserRead])
async def read_users(
    db: AsyncSession = Depends(deps.get_session),
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(deps.require_role(UserRole.ADMIN)),
):
    return await user_service.get_users(db, skip=skip, limit=limit)


@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(
    user_id: uuid.UUID,
    user_in: UserAdminUpdate,
    db: AsyncSession = Depends(deps.get_session),
    current_user=Depends(deps.require_role(UserRole.ADMIN)),
):
    db_user = await user_service.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return await user_service.admin_update_user(db, db_user=db_user, user_in=user_in)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_session),
    current_user=Depends(deps.require_role(UserRole.ADMIN)),
):
    db_user = await user_service.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    await user_service.delete_user(db, db_user=db_user)
    return None


@router.get("/analytics")
async def get_analytics(
    db: AsyncSession = Depends(deps.get_session),
    current_user=Depends(deps.require_role(UserRole.ADMIN)),
):
    users = await user_service.get_users(db, limit=1000)
    return {
        "total_users": len(users),
        "active_users": len([u for u in users if u.is_active]),
        "admin_count": len([u for u in users if u.role == UserRole.ADMIN]),
        "user_count": len([u for u in users if u.role == UserRole.USER]),
    }


@router.post("/users/{user_id}/reset-password", status_code=status.HTTP_200_OK)
async def admin_reset_password(
    user_id: uuid.UUID,
    new_password: str,
    db: AsyncSession = Depends(deps.get_session),
    current_user=Depends(deps.require_role(UserRole.ADMIN)),
):
    """
    Administrative override to reset a user's password.
    """
    from app.utils.hashing import get_password_hash
    db_user = await user_service.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.hashed_password = get_password_hash(new_password)
    db.add(db_user)
    await db.commit()
    return {"message": "User password reset successfully"}
