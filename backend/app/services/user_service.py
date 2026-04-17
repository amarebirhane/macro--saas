from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserAdminUpdate
from app.utils.hashing import get_password_hash

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def get_user_by_id(db: AsyncSession, user_id: str):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

async def create_user(db: AsyncSession, user_in: UserCreate, initial_role="USER"):
    if await get_user_by_email(db, user_in.email):
        return None
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=initial_role
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, user: User, user_in: UserUpdate):
    for field, value in user_in.model_dump(exclude_unset=True).items():
        if field == "password":
            user.hashed_password = get_password_hash(value)
        else:
            setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user

async def admin_update_user(db: AsyncSession, user_id: str, user_in: UserAdminUpdate):
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    for field, value in user_in.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user_id: str):
    user = await get_user_by_id(db, user_id)
    if user:
        await db.delete(user)
        await db.commit()
        return True
    return False
