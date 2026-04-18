import asyncio
from sqlmodel import Session, select
from app.core.database import engine
from app.models.user import User
from app.utils.hashing import get_password_hash
from datetime import datetime, timedelta

async def seed_data():
    print("Starting database seeding...")
    
    with Session(engine) as session:
        # 1. Create Admin
        admin_email = "admin@macro.com"
        admin_exists = session.exec(select(User).where(User.email == admin_email)).first()
        
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
            user_exists = session.exec(select(User).where(User.email == user_email)).first()
            
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
        
        session.commit()
    
    print("Seeding complete!")

if __name__ == "__main__":
    asyncio.run(seed_data())
