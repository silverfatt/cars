from fastapi import Query, Response
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter

from ....external.postgres.connection import get_connection_pool
from .core import add_car, get_car, get_cars_list_from_db
from .models import Car, CollectedCar

cars_router = APIRouter(prefix="/api/v1/cars", tags=["cars"])


@cars_router.post(
    "/api/v1/cars",
    responses={
        201: {"description": "Added new car to database"},
        502: {"description": "Database error"},
        500: {"description": "Unknown error"},
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


@cars_router.get(
    "/api/v1/cars/{id}",
    responses={
        200: {"description": "Successfully got car from database"},
        404: {"description": "Car not found"},
        502: {"description": "Database error"},
        500: {"description": "Unknown error"},
    },
)
async def get_car_view(
    response: Response,
    car_id: int = Query(ge=0),
    pool=Depends(get_connection_pool),
) -> CollectedCar:
    car = await get_car(pool, car_id)
    response.status_code = 200  # type: ignore
    return car


@cars_router.get(
    "/api/v1/cars",
    responses={
        200: {"description": "Successfully got cars from database"},
        502: {"description": "Database error"},
        500: {"description": "Unknown error"},
    },
)
async def get_cars_list(
    response: Response,
    offset: int = Query(ge=0),
    limit: int = Query(ge=0),
    pool=Depends(get_connection_pool),
) -> list[CollectedCar]:
    cars_list = await get_cars_list_from_db(pool, offset, limit)
    response.status_code = 200  # type: ignore
    return cars_list
