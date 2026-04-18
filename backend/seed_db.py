import asyncio
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.database import engine
from app.core.security import get_password_hash
from app.models.user import User


async def seed_data():
    print("Starting database seeding...")

    async with AsyncSession(engine) as session:
        # 1. Create or Update Admin
        admin_email = "admin@macro.com"
        result = await session.execute(select(User).where(User.email == admin_email))
        admin = result.scalar_one_or_none()

        if not admin:
            admin = User(
                email=admin_email,
                username="admin",
                first_name="System",
                last_name="Admin",
                hashed_password=get_password_hash("admin123"),
                role="ADMIN",
                is_active=True,
            )
            session.add(admin)
            print(f"Created Admin: {admin_email}")
        else:
            # Update existing admin with new fields if they are missing
            if not admin.username:
                admin.username = "admin"
                admin.first_name = "System"
                admin.last_name = "Admin"
                session.add(admin)
                print(f"Updated Admin {admin_email} with name/username")
            else:
                print(f"Admin {admin_email} already exists and is fully seeded")

        # 2. Create Dummy Users
        first_names = [
            "James",
            "Mary",
            "Robert",
            "Patricia",
            "John",
            "Jennifer",
            "Michael",
            "Linda",
            "William",
            "Elizabeth",
        ]
        last_names = [
            "Smith",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
            "Garcia",
            "Miller",
            "Davis",
            "Rodriguez",
            "Martinez",
        ]

        for i in range(1, 11):
            user_email = f"user{i}@macro.com"
            result = await session.execute(select(User).where(User.email == user_email))
            user = result.scalar_one_or_none()

            if not user:
                user = User(
                    email=user_email,
                    username=f"user{i}",
                    first_name=first_names[i - 1],
                    last_name=last_names[i - 1],
                    hashed_password=get_password_hash(f"password{i}"),
                    role="USER",
                    is_active=True,
                    created_at=datetime.utcnow() - timedelta(days=i),
                )
                session.add(user)
                print(f"Created User: {user_email}")
            elif not user.username:
                user.username = f"user{i}"
                user.first_name = first_names[i - 1]
                user.last_name = last_names[i - 1]
                session.add(user)
                print(f"Updated User: {user_email}")

        await session.commit()

    print("Seeding complete!")


if __name__ == "__main__":
    asyncio.run(seed_data())
