"""SQLAlchemy models for message."""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID as UUIDType

from sqlalchemy import Enum as SQLEnum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.pkg.models.sqlalchemy_models import Base
from app.pkg.models.v1.app.message import MessageStatusEnum


class Message(Base):
    __tablename__ = "message"

    message_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    text_template_id: Mapped[Optional[UUIDType]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("text_template.text_template_id", ondelete="SET NULL"),
        nullable=True,
    )
    correspondent_id: Mapped[Optional[UUIDType]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("correspondent.correspondent_id", ondelete="SET NULL"),
        nullable=True,
    )
    message_subject: Mapped[Optional[str]] = mapped_column(nullable=True)   # если без шаблона
    message_body: Mapped[Optional[str]] = mapped_column(nullable=True)      # если без шаблона
    message_data: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    message_status: Mapped[MessageStatusEnum] = mapped_column(
        SQLEnum(MessageStatusEnum, name="message_status_enum", native_enum=False),
        nullable=False,
        default=MessageStatusEnum.PENDING,
    )
    message_scheduled_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    message_create_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    message_update_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())

    template = relationship("TextTemplate", back_populates="messages")
    correspondent = relationship("Correspondent", back_populates="messages")
    recipients = relationship("Recipient", back_populates="message", cascade="all, delete-orphan")

