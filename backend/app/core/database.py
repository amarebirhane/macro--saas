from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

# SQLModel/SQLAlchemy Async Engine
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

# Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    # In practice, use Alembic for migrations.
    # This remains for quick dev sync if needed,
    # but we will prioritize Alembic as per the prompt.
    async with engine.begin():
        # await conn.run_sync(SQLModel.metadata.create_all)
        pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
