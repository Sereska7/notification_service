"""SQLAlchemy models for delivery."""

import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID as UUIDType

from sqlalchemy import Enum as SQLEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.pkg.models.sqlalchemy_models import Base
from app.pkg.models.v1.app.delivery import DeliveryStatusEnum


class Delivery(Base):
    __tablename__ = "delivery"

    delivery_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    recipient_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("recipient.recipient_id", ondelete="CASCADE"),
        nullable=False,
    )
    delivery_attempt_no: Mapped[int] = mapped_column(nullable=False, default=1)
    delivery_provider: Mapped[str] = mapped_column(nullable=False)  # ses/twilio/fcm/...
    delivery_status: Mapped[DeliveryStatusEnum] = mapped_column(
        SQLEnum(DeliveryStatusEnum, name="delivery_status_enum", native_enum=False),
        nullable=False,
        default=DeliveryStatusEnum.QUEUED,
    )
    delivery_provider_message_id: Mapped[Optional[str]] = mapped_column(nullable=True)
    delivery_error_code: Mapped[Optional[str]] = mapped_column(nullable=True)
    delivery_error_message: Mapped[Optional[str]] = mapped_column(nullable=True)
    delivery_queued_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    delivery_sent_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    delivery_finalized_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    recipient = relationship("Recipient", back_populates="deliveries")
