"""Routes for TelegramCorrespondent module."""

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status

from app.internal.services import Services
from app.internal.services.v1 import EmailCorrespondentService, TelegramCorrespondentService
from app.pkg.models import v1 as models
from app.pkg.models.base.request_id_route import RequestIDRoute

router = APIRouter(
    prefix="/telegram_correspondent",
    tags=["TelegramCorrespondent"],
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
    telegram_correspondent_service: TelegramCorrespondentService = Depends(Provide[Services.v1.telegram_correspondent_service]),
) -> models.TelegramCorrespondentResponse:
    return await telegram_correspondent_service.create_telegram_correspondent(cmd)
