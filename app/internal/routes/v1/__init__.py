"""Routes for version 1 of the API."""

from fastapi import APIRouter


router = APIRouter(
    prefix="/v1",
)

routes = sorted(
    [],
    key=lambda r: r.prefix,
)

for route in routes:
    router.include_router(route)
