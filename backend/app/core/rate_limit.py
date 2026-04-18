import logging
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings

# Initialize the limiter with a fallback for development environments
def get_limiter():
    storage_uri = settings.REDIS_URL
    
    # In development, we can fallback to memory if Redis is down
    if settings.ENVIRONMENT == "development":
        import redis
        try:
            # Quick ping to see if Redis is there
            r = redis.from_url(storage_uri, socket_connect_timeout=1)
            r.ping()
        except Exception:
            logging.warning(f"Redis not found at {storage_uri}. Falling back to memory:// for rate limiting.")
            storage_uri = "memory://"
            
    return Limiter(key_func=get_remote_address, storage_uri=storage_uri)

limiter = get_limiter()
