"""SQLAlchemy models for recipient."""

import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID as UUIDType

from sqlalchemy import Enum as SQLEnum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.pkg.models.sqlalchemy_models import Base
from app.pkg.models.v1.app.message import ChannelEnum


class Recipient(Base):
    __tablename__ = "recipient"

    recipient_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    message_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("message.message_id", ondelete="CASCADE"),
        nullable=False,
    )
    recipient_user_id: Mapped[Optional[UUIDType]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    recipient_channel: Mapped[ChannelEnum] = mapped_column(
        SQLEnum(ChannelEnum, name="channel_enum", native_enum=False),
        nullable=False,
    )
    recipient_address: Mapped[str] = mapped_column(nullable=False)  # email/phone/device token/user_id (web)
    recipient_locale: Mapped[Optional[str]] = mapped_column(nullable=True)
    recipient_timezone: Mapped[Optional[str]] = mapped_column(nullable=True)
    recipient_create_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    message = relationship("Message", back_populates="recipients")
    deliveries = relationship(
        "Delivery",
        back_populates="recipient",
        cascade="all, delete-orphan",
    )