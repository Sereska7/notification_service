"""Delivery repository implementation."""

from sqlalchemy import select, update, func

from app.internal.repository.repository import Repository
from app.internal.repository.v1.postgresql.connection import get_connection
from app.internal.repository.v1.postgresql.handlers.collect_response import (
    collect_response,
)
from app.pkg.models import v1 as models

__all__ = ["DeliveryRepository"]


class DeliveryRepository(Repository):
    """Delivery repository implementation."""