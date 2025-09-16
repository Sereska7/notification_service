"""SQLAlchemy model for text template."""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID as UUIDType

from sqlalchemy import Enum as SQLEnum, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.pkg.models.sqlalchemy_models import Base
from app.pkg.models.v1 import ChannelEnum


class TextTemplate(Base):
    __tablename__ = "text_template"

    text_template_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    text_template_code: Mapped[str] = mapped_column(nullable=False, index=True)
    text_template_is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    text_template_subject: Mapped[Optional[str]] = mapped_column(nullable=True)
    text_template_content: Mapped[str] = mapped_column(nullable=False)
    text_template_variables: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    text_template_channel: Mapped[ChannelEnum] = mapped_column(
        SQLEnum(ChannelEnum, name="template_channel_enum", native_enum=False),
        nullable=False
    )
    text_template_create_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    text_template_update_at: Mapped[Optional[datetime]] = mapped_column(
        onupdate=func.now()
    )
