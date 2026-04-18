from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings

# Initialize the limiter using Redis for multi-worker synchronization
limiter = Limiter(
    key_func=get_remote_address, 
    storage_uri=settings.REDIS_URL
)
