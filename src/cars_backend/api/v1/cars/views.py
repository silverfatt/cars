from fastapi import Response
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter

from ....external.postgres.connection import get_connection_pool
from .core import add_car
from .models import Car

cars_router = APIRouter(prefix="/api/v1/cars", tags=["cars"])


@cars_router.get("/api/v1/cars")
async def test_route() -> str:
    return "ok"


@cars_router.post(
    "/api/v1/cars",
    responses={
        502: {"description": "Error during making a query to postgres"},
        200: {"description": "Found number in database"},
        201: {"description": "Added new number to database"},
        403: {"description": "Service is not in access users"},
    },
)
async def add_car_view(
    car_to_add: Car,
    response: Response,
    pool=Depends(get_connection_pool),
) -> str:
    await add_car(pool, car_to_add)
    response.status_code = 201  # type: ignore
    return "ok"
