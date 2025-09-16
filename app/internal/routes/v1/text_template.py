"""Routes for TextTemplate module."""

from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status, Query

from app.internal.services import Services
from app.internal.services.v1 import TextTemplateService
from app.pkg.models import v1 as models
from app.pkg.models.base.request_id_route import RequestIDRoute
from app.pkg.models.v1 import ChannelEnum

router = APIRouter(
    prefix="/text-template",
    tags=["Text Template"],
    route_class=RequestIDRoute
)


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=models.TextTemplate,
    description="""
    """,
)
@inject
async def create_text_template(
    cmd: models.TextTemplateCreateCommand,
    text_template_service: TextTemplateService = Depends(
        Provide[Services.v1.text_template_service]),
) -> models.TextTemplate:
    return await text_template_service.create_text_template(cmd)

@router.get(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=list[models.TextTemplate],
    description="""
    """,
)
@inject
async def get_text_template(
    text_template_id: Annotated[
        UUID, Query(..., description="Text template id.")] = None,
    text_template_is_active: Annotated[
        bool, Query(..., description="Text template is active.")] = None,
    text_template_code: Annotated[
        str, Query(..., description="Text template code.")] = None,
    text_template_subject: Annotated[
        str, Query(..., description="Text template subject.")] = None,
    text_template_channel: Annotated[
        ChannelEnum, Query(..., description="Text template channel.")] = None,
    text_template_service: TextTemplateService = Depends(
        Provide[Services.v1.text_template_service]),
) -> list[models.TextTemplate]:
    query = models.TextTemplateReadQuery(
        text_template_id=text_template_id,
        text_template_is_active=text_template_is_active,
        text_template_code=text_template_code,
        text_template_subject=text_template_subject,
        text_template_channel=text_template_channel,
    )
    return await text_template_service.get_text_template(query)


@router.patch(
    "/update",
    status_code=status.HTTP_200_OK,
    response_model=models.TextTemplate,
    description="""
    """
)
@inject
async def update_text_template(
    cmd: models.TextTemplateUpdateCommand,
    text_template_service: TextTemplateService = Depends(
        Provide[Services.v1.text_template_service]
    )
) -> models.TextTemplate:
    return await text_template_service.update_text_template(cmd)


@router.delete(
    "/delete",
    status_code=status.HTTP_200_OK,
    response_model=models.TextTemplate,
    description="""
    """
)
@inject
async def delete_text_template(
    cmd: models.TextTemplateDeleteCommand,
    text_template_service: TextTemplateService = Depends(
        Provide[Services.v1.text_template_service]
    )
) -> models.TextTemplate:
    return await text_template_service.delete_text_template(cmd)
