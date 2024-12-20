from fastapi import Query, Response
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter

from ....external.postgres.connection import get_connection_pool
from ..auth.auth import get_current_active_user
from ..auth.models import User

dashboards_router = APIRouter(prefix="/api/v1/dashboards", tags=["dashboards"])


@dashboards_router.get(
    "/",
    responses={
        200: {"description": "Successfully predicted"},
    },
)
async def predict_car(
    response: Response,
    current_user: User = Depends(get_current_active_user),
) -> str:
    return "ok"
