from urllib.parse import urlparse

from arq.connections import RedisSettings

from app.core.config import settings
from app.core.email import send_email


async def send_welcome_email_task(ctx: dict, email: str, name: str) -> bool:
    """
    Background task to send a welcome email.
    """
    print(f"[{ctx['job_id']}] Sending welcome email to {email}...")
    await send_email(
        email_to=email,
        subject=f"Welcome to {settings.PROJECT_NAME}!",
        template_name="welcome.html",
        template_body={"name": name, "project_name": settings.PROJECT_NAME},
    )
    return True


async def send_verification_email_task(ctx: dict, email: str, name: str, link: str) -> bool:
    """
    Background task to send a verification email.
    """
    print(f"[{ctx['job_id']}] Sending verification email to {email}...")
    await send_email(
        email_to=email,
        subject=f"Verify your email - {settings.PROJECT_NAME}",
        template_name="verify.html",
        template_body={"name": name, "link": link, "project_name": settings.PROJECT_NAME},
    )
    return True


async def send_password_reset_email_task(ctx: dict, email: str, name: str, link: str) -> bool:
    """
    Background task to send a password reset email.
    """
    print(f"[{ctx['job_id']}] Sending password reset email to {email}...")
    await send_email(
        email_to=email,
        subject=f"Reset your password - {settings.PROJECT_NAME}",
        template_name="reset.html",
        template_body={"name": name, "link": link, "project_name": settings.PROJECT_NAME},
    )
    return True


async def startup(ctx: dict) -> None:
    print("ARQ Worker Starting up...")


async def shutdown(ctx: dict) -> None:
    print("ARQ Worker Shutting down...")


# Parse redis url properly for arq
parsed_url = urlparse(settings.REDIS_URL)


class WorkerSettings:
    functions = [
        send_welcome_email_task,
        send_verification_email_task,
        send_password_reset_email_task,
    ]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings(
        host=parsed_url.hostname or "localhost",
        port=parsed_url.port or 6379,
        database=int(parsed_url.path.strip("/"))
        if parsed_url.path not in ("", "/")
        else 0,
    )
