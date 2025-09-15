"""Routes for EmailCorrespondent module."""

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status

from app.internal.services import Services
from app.internal.services.v1 import EmailCorrespondentService
from app.pkg.models import v1 as models
from app.pkg.models.base.request_id_route import RequestIDRoute

router = APIRouter(
    prefix="/email_correspondent",
    tags=["EmailCorrespondent"],
    route_class=RequestIDRoute
)


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=models.EmailCorrespondentResponse,
    description="""
    Description: Create new correspondent.
    Used: Method is used to create correspondent.
    """,
)
@inject
async def create_correspondent(
    cmd: models.EmailCorrespondentCreateCommand,
    email_correspondent_service: EmailCorrespondentService = Depends(Provide[Services.v1.email_correspondent_service]),
) -> models.EmailCorrespondentResponse:
    return await email_correspondent_service.create_correspondent(cmd)