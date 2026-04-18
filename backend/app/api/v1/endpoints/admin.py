import math

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_role
from app.core.database import get_db
from app.schemas.common import PaginatedResponse
from app.schemas.user import UserAdminUpdate, UserOut
from app.services.audit_service import audit_service
from app.services.user_service import (
    admin_update_user,
    delete_user,
    get_users_paginated,
)

router = APIRouter()


@router.get(
    "/users",
    response_model=PaginatedResponse[UserOut],
    dependencies=[Depends(require_role("ADMIN"))],
)
async def read_users(page: int = 1, size: int = 20, db: AsyncSession = Depends(get_db)):
    skip = (page - 1) * size
    items, total = await get_users_paginated(db, skip=skip, limit=size)

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size) if total > 0 else 1,
    )


@router.put(
    "/users/{user_id}",
    response_model=UserOut,
    dependencies=[Depends(require_role("ADMIN"))],
)
async def update_user_by_admin(
    user_id: str,
    user_in: UserAdminUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user = await admin_update_user(db, user_id, user_in)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await audit_service.create_log(
        db,
        action="UPDATE_USER",
        resource=f"user:{user_id}",
        user_id=current_user.id,
        metadata_json=user_in.model_dump(exclude_unset=True),
    )
    return user


@router.delete("/users/{user_id}", dependencies=[Depends(require_role("ADMIN"))])
async def delete_user_by_admin(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    success = await delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    await audit_service.create_log(
        db, action="DELETE_USER", resource=f"user:{user_id}", user_id=current_user.id
    )
    return {"detail": "User deleted successfully"}


@router.get("/analytics", dependencies=[Depends(require_role("ADMIN"))])
async def get_analytics(
    db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    await audit_service.create_log(
        db,
        action="ACCESS_ANALYTICS",
        resource="system:analytics",
        user_id=current_user.id,
    )
    # Fetch a reasonable number of users for stats, or optimize with specific count queries in production
    users, total = await get_users_paginated(db, limit=1000)
    return {
        "total_users": total,
        "active_users": len([u for u in users if u.is_active]),
        "admin_count": len([u for u in users if u.role == "ADMIN"]),
        "regular_users": len([u for u in users if u.role == "USER"]),
    }
