from pathlib import Path
from typing import Any, Dict

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from app.core.config import settings
from app.core.logging_config import logger

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.EMAILS_FROM_EMAIL or "info@example.com",
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST or "localhost",
    MAIL_FROM_NAME=settings.EMAILS_FROM_NAME or settings.PROJECT_NAME,
    MAIL_STARTTLS=settings.SMTP_TLS,
    MAIL_SSL_TLS=not settings.SMTP_TLS,
    USE_CREDENTIALS=True if settings.SMTP_USER else False,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
    SUPPRESS_SEND=True if settings.ENVIRONMENT == "development" and not settings.SMTP_USER else False
)

fastmail = FastMail(conf)

async def send_email(
    email_to: str,
    subject: str,
    template_name: str,
    template_body: Dict[str, Any],
) -> None:
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=template_body,
        subtype=MessageType.html,
    )
    
    if conf.SUPPRESS_SEND:
        logger.info(f"📧 [DEV MODE] Email suppressed. Subject: {subject}, To: {email_to}")
        logger.info(f"Context: {template_body}")
        # In suppressed mode, fastapi_mail still renders but doesn't send
        await fastmail.send_message(message, template_name=template_name)
    else:
        await fastmail.send_message(message, template_name=template_name)
