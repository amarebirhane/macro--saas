from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit import AuditLog
from typing import Optional, Dict
import uuid

class AuditService:
    @staticmethod
    async def create_log(
        db: AsyncSession,
        action: str,
        resource: str,
        user_id: Optional[uuid.UUID] = None,
        metadata_json: Optional[Dict] = None
    ):
        db_log = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            metadata_json=metadata_json or {}
        )
        db.add(db_log)
        await db.commit()
        await db.refresh(db_log)
        return db_log

audit_service = AuditService()
