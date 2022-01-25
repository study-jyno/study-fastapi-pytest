from typing import List, Optional

from fastapi import APIRouter, Depends

from pydantic import BaseModel
from starlette.responses import JSONResponse

from app.routers.auth import router as user_router
from app.routers.item import router as item_router


class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMessage]]


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)

# WARNING: Don't use this unless you want unauthenticated routes
authenticated_organization_api_router = APIRouter()

authenticated_organization_api_router.include_router(user_router)
authenticated_organization_api_router.include_router(item_router)


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}


api_router.include_router(
    authenticated_organization_api_router
)
