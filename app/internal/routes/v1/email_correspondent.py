"""Routes for EmailCorrespondent module."""

from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status, Query

from app.internal.services import Services
from app.internal.services.v1 import EmailCorrespondentService
from app.pkg.models import v1 as models
from app.pkg.models.base.request_id_route import RequestIDRoute

router = APIRouter(
    prefix="/email_correspondent",
    tags=["Email Correspondent"],
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


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[models.EmailCorrespondentResponse],
    description="""
    Description: Get list email correspondents.
    Used: Method is used to get email correspondents.
    """
)
@inject
async def get_email_correspondents(
    email_correspondent_id: Annotated[UUID, Query(..., description="Email correspondent id.")] = None,
    email_correspondent_name: Annotated[str, Query(..., description="Email correspondent name")] = None,
    email_correspondent_is_active: Annotated[bool, Query(..., description="Email correspondent is active")] = None,
    email_correspondent_service: EmailCorrespondentService = Depends(Provide[Services.v1.email_correspondent_service]),
) -> list[models.EmailCorrespondentResponse]:
    query = models.EmailCorrespondentReadQuery(
            email_correspondent_id=email_correspondent_id,
            email_correspondent_name=email_correspondent_name,
            email_correspondent_is_active=email_correspondent_is_active,
        )
    return await email_correspondent_service.get_email_correspondent(query)


@router.patch(
    "/update",
    status_code=status.HTTP_200_OK,
    response_model=models.EmailCorrespondentResponse,
    description="""
    Description: Update correspondent.
    Used: Method is used to update correspondent.
    """
)
@inject
async def update_email_correspondent(
    cmd: models.EmailCorrespondentUpdateCommand,
    email_correspondent_service: EmailCorrespondentService = Depends(Provide[Services.v1.email_correspondent_service])
) -> models.EmailCorrespondentResponse:
    return await email_correspondent_service.update_email_correspondent(cmd)


@router.delete(
    "/delete",
    status_code=status.HTTP_200_OK,
    response_model=models.EmailCorrespondentResponse,
    description="""
    Description: Delete correspondent.
    Used: Method is used to delete correspondent.
    """
)
@inject
async def delete_email_correspondent(
    cmd: models.EmailCorrespondentDeleteCommand,
    email_correspondent_service: EmailCorrespondentService = Depends(Provide[Services.v1.email_correspondent_service])
) -> models.EmailCorrespondentResponse:
    return await email_correspondent_service.delete_email_correspondent(cmd)

