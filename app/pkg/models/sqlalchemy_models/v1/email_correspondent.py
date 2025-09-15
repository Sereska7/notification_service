"""SQLAlchemy models for email correspondent."""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID as UUIDType

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.pkg.models.sqlalchemy_models import Base


class EmailCorrespondent(Base):
    __tablename__ = "email_correspondent"

    email_correspondent_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email_correspondent_name: Mapped[str] = mapped_column(nullable=False)
    email_correspondent_is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    email_host: Mapped[str] = mapped_column(nullable=False)
    email_port: Mapped[int] = mapped_column(nullable=False)
    email_username: Mapped[str] = mapped_column(nullable=False)
    email_password: Mapped[str] = mapped_column(nullable=False)
    email_correspondent_create_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    email_correspondent_update_at: Mapped[Optional[datetime]] = mapped_column(
        onupdate=func.now()
    )
