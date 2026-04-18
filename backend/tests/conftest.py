import asyncio
import pytest
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from asgi_lifespan import LifespanManager

from app.main import app
from app.api.deps import get_session
from app.core.config import settings

# Test database URL (using a different database for tests)
TEST_DATABASE_URL = settings.DATABASE_URL.replace("/macro", "/macro_test")

# Create a test engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)

# Create a test session factory
TestAsyncSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def db_setup():
    """Create the database tables for tests."""
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest.fixture
async def db_session(db_setup) -> AsyncGenerator[AsyncSession, None]:
    """Provide a test database session."""
    async with TestAsyncSessionLocal() as session:
        yield session

@pytest.fixture
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    """Provide a test client with an overridden database session."""
    
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session
    
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            yield ac
            
    app.dependency_overrides.clear()
