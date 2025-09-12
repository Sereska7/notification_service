"""SQLAlchemy models for correspondent."""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID as UUIDType

from sqlalchemy import Enum as SQLEnum, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.pkg.models.sqlalchemy_models import Base
from app.pkg.models.v1.app.message import ChannelEnum


class Correspondent(Base):
    __tablename__ = "correspondent"

    correspondent_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    correspondent_channel: Mapped[ChannelEnum] = mapped_column(
        SQLEnum(ChannelEnum, name="channel_enum", native_enum=False),
        nullable=False,
        index=True,
    )
    correspondent_name: Mapped[str] = mapped_column(nullable=False)
    correspondent_from_address: Mapped[Optional[str]] = mapped_column(nullable=True)
    correspondent_provider: Mapped[str] = mapped_column(nullable=False)
    correspondent_config: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    correspondent_is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    correspondent_create_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    correspondent_update_at: Mapped[Optional[datetime]] = mapped_column(
        onupdate=func.now()
    )
    messages = relationship("Message", back_populates="correspondent")
