from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import get_user_by_email
from app.utils.hashing import verify_password

async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
