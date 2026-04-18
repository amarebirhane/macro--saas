from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas.user import UserOut, UserAdminUpdate
from app.api.deps import require_role
from app.services.user_service import get_all_users, admin_update_user, delete_user
from app.services.audit_service import audit_service
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/users", response_model=List[UserOut], dependencies=[Depends(require_role("ADMIN"))])
async def read_all_users(db: AsyncSession = Depends(get_db)):
    return await get_all_users(db)

@router.put("/users/{user_id}", response_model=UserOut, dependencies=[Depends(require_role("ADMIN"))])
async def update_user_by_admin(
    user_id: str, 
    user_in: UserAdminUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user = await admin_update_user(db, user_id, user_in)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await audit_service.create_log(
        db,
        action="UPDATE_USER",
        resource=f"user:{user_id}",
        user_id=current_user.id,
        metadata_json=user_in.model_dump(exclude_unset=True)
    )
    return user

@router.delete("/users/{user_id}", dependencies=[Depends(require_role("ADMIN"))])
async def delete_user_by_admin(
    user_id: str, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    success = await delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    
    await audit_service.create_log(
        db,
        action="DELETE_USER",
        resource=f"user:{user_id}",
        user_id=current_user.id
    )
    return {"detail": "User deleted successfully"}

@router.get("/analytics", dependencies=[Depends(require_role("ADMIN"))])
async def get_analytics(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    await audit_service.create_log(
        db,
        action="ACCESS_ANALYTICS",
        resource="system:analytics",
        user_id=current_user.id
    )
    users = await get_all_users(db)
    return {
        "total_users": len(users),
        "active_users": len([u for u in users if u.is_active]),
        "admins": len([u for u in users if u.role == "ADMIN"]),
        "regular_users": len([u for u in users if u.role == "USER"])
    }
