import asyncio
from typing import Any
from arq import create_pool
from arq.connections import RedisSettings
from app.core.config import settings

async def send_welcome_email(ctx: dict, email: str, name: str) -> bool:
    """
    Dummy background task to simulate sending an email.
    In phase 3 we will integrate fastapi-mail here.
    """
    print(f"[{ctx['job_id']}] Sending welcome email asynchronously to {name} <{email}>...")
    await asyncio.sleep(2)  # Simulate network latency
    print(f"[{ctx['job_id']}] Successfully sent email to {email}")
    return True

async def startup(ctx: dict) -> None:
    print("ARQ Worker Starting up...")

async def shutdown(ctx: dict) -> None:
    print("ARQ Worker Shutting down...")

# Parse redis url properly for arq
from urllib.parse import urlparse
parsed_url = urlparse(settings.REDIS_URL)

class WorkerSettings:
    functions = [send_welcome_email]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings(
        host=parsed_url.hostname or 'localhost',
        port=parsed_url.port or 6379,
        database=int(parsed_url.path.strip('/')) if parsed_url.path not in ('', '/') else 0
    )
    
