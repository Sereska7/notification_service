"""SQLAlchemy models for message."""

import uuid
from datetime import datetime
from uuid import UUID as UUIDType

from sqlalchemy import Enum as SQLEnum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.pkg.models.sqlalchemy_models import Base
from app.pkg.models.v1.app.message import MessageStatusEnum, ChannelEnum


class Message(Base):
    __tablename__ = "message"

    message_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    recipient_id: Mapped[UUIDType] = mapped_column(
        ForeignKey("recipient.recipient_id"),
        nullable=False,
        index=True,
    )
    message_body: Mapped[str] = mapped_column(nullable=False)
    message_status: Mapped[MessageStatusEnum] = mapped_column(nullable=False)
    message_channel: Mapped[ChannelEnum] = mapped_column(
        SQLEnum(ChannelEnum, name="channel_enum", native_enum=False),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    recipient = relationship("Recipient", back_populates="messages", passive_deletes=True)
