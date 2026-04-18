import asyncio
import pytest
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from asgi_lifespan import LifespanManager

from app.main import app
from app.api.deps import get_session
from app.core.redis import get_arq_pool
from unittest.mock import AsyncMock

# SQLite for local testing (fast and isolated)
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

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

    async def mock_get_arq_pool():
        return AsyncMock()

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_arq_pool] = mock_get_arq_pool
    
    # Disable rate limiting in tests
    app.state.limiter.enabled = False
    
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac
            
    app.dependency_overrides.clear()
    app.state.limiter.enabled = True
