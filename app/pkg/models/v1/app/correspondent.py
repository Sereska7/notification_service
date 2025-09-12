"""Correspondent models."""

from datetime import datetime
from uuid import UUID

from pydantic.fields import Field

from app.pkg.models.base import BaseModel
from app.pkg.models.base.optional_field import create_optional_fields_class

__all__ = [

]


class BaseCorrespondent(BaseModel):
    """Base model for Correspondent."""


class CorrespondentFields:
    """Correspondent fields."""