"""SQLAlchemy models for telegram correspondent."""

import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID as UUIDType

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.pkg.models.sqlalchemy_models import Base


class TelegramCorrespondent(Base):
    __tablename__ = "telegram_correspondent"

    telegram_correspondent_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    telegram_correspondent_name: Mapped[str] = mapped_column(nullable=False)
    telegram_correspondent_is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    telegram_bot_token: Mapped[str] = mapped_column(nullable=False)
    telegram_correspondent_create_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    telegram_correspondent_update_at: Mapped[Optional[datetime]] = mapped_column(
        onupdate=func.now()
    )
