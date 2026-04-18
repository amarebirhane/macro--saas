from urllib.parse import urlparse

from arq import create_pool
from arq.connections import RedisSettings

from app.core.config import settings


async def get_arq_pool():
    parsed_url = urlparse(settings.REDIS_URL)
    return await create_pool(
        RedisSettings(
            host=parsed_url.hostname or "localhost",
            port=parsed_url.port or 6379,
            database=int(parsed_url.path.strip("/")) if parsed_url.path not in ("", "/") else 0,
        )
    )
