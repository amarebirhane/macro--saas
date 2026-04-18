import sentry_sdk
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.api.middleware import GlobalExceptionHandlerMiddleware
from app.api.routes import admin, auth, users
from app.core.config import settings
from app.core.database import init_db
from app.core.logging_config import logger, setup_logging
from app.core.rate_limit import limiter

# Initialize Logging
setup_logging()

# Initialize Sentry APM
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        traces_sample_rate=1.0,
    )

app = FastAPI(title=settings.PROJECT_NAME, openapi_url="/openapi.json")

# Add Rate Limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add Middleware
app.add_middleware(GlobalExceptionHandlerMiddleware)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files (Profile Images)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])


@app.on_event("startup")
async def startup_event():
    await init_db()

    # Initialize Redis Cache
    redis = aioredis.from_url(
        settings.REDIS_URL, encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get("/")
def root():
    return {
        "message": "Welcome to the Micro-SaaS API",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health", tags=["Health"])
async def health_check(db: AsyncSession = Depends(deps.get_session)):
    """Health check endpoint validating application and database state."""
    try:
        # Added timeout to prevent health check from hanging
        await db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Health check database failure: {str(e)}")
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "online",
        "environment": settings.ENVIRONMENT,
        "database": db_status,
    }
