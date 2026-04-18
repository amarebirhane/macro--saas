from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate
from app.services import user_service
from app.utils.storage import storage_service

router = APIRouter()


@router.get("/me", response_model=UserRead)
async def read_user_me(current_user: User = Depends(deps.get_current_user)):
    return current_user


@router.put("/me", response_model=UserRead)
async def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_session),
):
    return await user_service.update_user(db, db_user=current_user, user_in=user_in)


@router.post("/me/avatar", response_model=UserRead)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_session),
):
    """
    Upload and set a profile image for the current user.
    """
    try:
        # Delete old avatar if exists
        if current_user.avatar_url:
            storage_service.delete_old_avatar(current_user.avatar_url)

        # Save new avatar
        filename = await storage_service.save_avatar(file)

        # Update user record
        current_user.avatar_url = filename
        db.add(current_user)
        await db.commit()
        await db.refresh(current_user)

        return current_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to process image.")
