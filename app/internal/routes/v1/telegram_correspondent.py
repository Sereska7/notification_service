"""Routes for TelegramCorrespondent module."""

from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status, Query

from app.internal.services import Services
from app.internal.services.v1 import TelegramCorrespondentService
from app.pkg.models import v1 as models
from app.pkg.models.base.request_id_route import RequestIDRoute

router = APIRouter(
    prefix="/telegram_correspondent",
    tags=["Telegram Correspondent"],
    route_class=RequestIDRoute
)


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=models.TelegramCorrespondentResponse,
    description="""
    Description: Create new telegram correspondent.
    Used: Method is used to create correspondent.
    """,
)
@inject
async def create_correspondent(
    cmd: models.TelegramCorrespondentCreateCommand,
    telegram_correspondent_service: TelegramCorrespondentService = Depends(
        Provide[Services.v1.telegram_correspondent_service]),
) -> models.TelegramCorrespondentResponse:
    return await telegram_correspondent_service.create_telegram_correspondent(cmd)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[models.TelegramCorrespondentResponse],
    description="""
    Description: Get all telegram correspondents.
    Used: Method is used to get all telegram correspondents.
    """
)
@inject
async def get_telegram_correspondents(
    telegram_correspondent_id: Annotated[UUID, Query(..., description="Telegram correspondent id.")] = None,
    telegram_correspondent_name: Annotated[str, Query(..., description="Telegram correspondent name")] = None,
    telegram_correspondent_is_active: Annotated[bool, Query(..., description="Telegram correspondent is active")] = None,
    telegram_correspondent_service: TelegramCorrespondentService = Depends(
        Provide[Services.v1.telegram_correspondent_service]),
) -> list[models.TelegramCorrespondentResponse]:
    query = models.TelegramCorrespondentReadQuery(
            telegram_correspondent_id=telegram_correspondent_id,
            telegram_correspondent_name=telegram_correspondent_name,
            telegram_correspondent_is_active=telegram_correspondent_is_active,
        )
    return await telegram_correspondent_service.get_telegram_correspondent(query)


@router.patch(
    "/update",
    status_code=status.HTTP_200_OK,
    response_model=models.TelegramCorrespondentResponse,
    description="""
    Description: Update telegram correspondent.
    Used: Method is used to update correspondent.
    """
)
@inject
async def update_telegram_correspondent(
    cmd: models.TelegramCorrespondentUpdateCommand,
    telegram_correspondent_service: TelegramCorrespondentService = Depends(
        Provide[Services.v1.telegram_correspondent_service]),
) -> models.TelegramCorrespondentResponse:
    return await telegram_correspondent_service.update_telegram_correspondent(cmd)


@router.delete(
    "/delete",
    status_code=status.HTTP_200_OK,
    response_model=models.TelegramCorrespondentResponse,
    description="""
    Description: Delete telegram correspondent.
    Used: Method is used to delete correspondent.
    """
)
@inject
async def delete_telegram_correspondent(
    cmd: models.TelegramCorrespondentDeleteCommand,
    telegram_correspondent_service: TelegramCorrespondentService = Depends(
            Provide[Services.v1.telegram_correspondent_service]),
) -> models.TelegramCorrespondentResponse:
    return await telegram_correspondent_service.delete_telegram_correspondent(cmd)
