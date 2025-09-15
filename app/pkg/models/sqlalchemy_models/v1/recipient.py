"""SQLAlchemy models for recipient."""

import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID as UUIDType

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.pkg.models.sqlalchemy_models import Base


class Recipient(Base):
    __tablename__ = "recipient"

    recipient_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    recipient_user_id: Mapped[Optional[UUIDType]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    recipient_address: Mapped[str] = mapped_column(nullable=False)
    recipient_locale: Mapped[Optional[str]] = mapped_column(nullable=True)
    recipient_timezone: Mapped[Optional[str]] = mapped_column(nullable=True)
    recipient_create_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    messages = relationship(
        "Message",
        back_populates="recipient",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    deliveries = relationship(
        "Delivery",
        back_populates="recipient",
        cascade="all, delete-orphan",
    )