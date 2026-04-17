from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import UserOut, UserUpdate
from app.api.deps import get_current_active_user
from app.services.user_service import update_user

router = APIRouter()

@router.get("/me", response_model=UserOut)
async def read_user_me(current_user = Depends(get_current_active_user)):
    return current_user

@router.put("/me", response_model=UserOut)
async def update_user_me(
    user_in: UserUpdate, 
    current_user = Depends(get_current_active_user), 
    db: AsyncSession = Depends(get_db)
):
    return await update_user(db, current_user, user_in)
