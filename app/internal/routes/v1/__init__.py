"""Routes for version 1 of the API."""

from fastapi import APIRouter
from app.internal.routes.v1.email_correspondent import router as email_correspondent_router
from app.internal.routes.v1.telegram_correspondent import router as telegram_correspondent_router
from app.internal.routes.v1.text_template import router as text_template_router


router = APIRouter(
    prefix="/v1",
)

routes = sorted(
    [email_correspondent_router,
    telegram_correspondent_router,
    text_template_router
    ],
    key=lambda r: r.prefix,
)

for route in routes:
    router.include_router(route)
