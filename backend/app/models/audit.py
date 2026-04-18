from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid
from typing import Optional, Dict
from sqlalchemy import Column, JSON

class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False
    )
    user_id: Optional[uuid.UUID] = Field(default=None, index=True)
    action: str = Field(nullable=False)
    resource: str = Field(nullable=False)
    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    metadata_json: Optional[Dict] = Field(default_factory=dict, sa_column=Column(JSON))
