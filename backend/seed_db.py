import asyncio
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import engine
from app.models.user import User
from app.utils.hashing import get_password_hash
from datetime import datetime, timedelta

async def seed_data():
    print("Starting database seeding...")
    
    async with AsyncSession(engine) as session:
        # 1. Create Admin
        admin_email = "admin@macro.com"
        result = await session.execute(select(User).where(User.email == admin_email))
        admin_exists = result.scalar_one_or_none()
        
        if not admin_exists:
            admin = User(
                email=admin_email,
                hashed_password=get_password_hash("admin123"),
                role="ADMIN",
                is_active=True
            )
            session.add(admin)
            print(f"Created Admin: {admin_email}")
        else:
            print(f"Admin {admin_email} already exists")

        # 2. Create Dummy Users
        for i in range(1, 11):
            user_email = f"user{i}@macro.com"
            result = await session.execute(select(User).where(User.email == user_email))
            user_exists = result.scalar_one_or_none()
            
            if not user_exists:
                user = User(
                    email=user_email,
                    hashed_password=get_password_hash(f"password{i}"),
                    role="USER",
                    is_active=True,
                    created_at=datetime.utcnow() - timedelta(days=i)
                )
                session.add(user)
                print(f"Created User: {user_email}")
        
        await session.commit()
    
    print("Seeding complete!")

if __name__ == "__main__":
    asyncio.run(seed_data())
