from fastapi import Query, Response
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter

from ....external.postgres.connection import get_connection_pool
from ..auth.auth import get_current_active_user
from ..auth.models import User
from .core import add_car, delete_car, get_car, get_cars_list
from .models import Car, CollectedCar

cars_router = APIRouter(prefix="/api/v1/cars", tags=["cars"])


@cars_router.post(
    "/",
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
    current_user: User = Depends(get_current_active_user),
) -> str:
    await add_car(pool, car_to_add)
    response.status_code = 201  # type: ignore
    return "ok"


@cars_router.get(
    "/{id}",
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
    current_user: User = Depends(get_current_active_user),
) -> CollectedCar:
    car = await get_car(pool, car_id)
    response.status_code = 200  # type: ignore
    return car


@cars_router.get(
    "/",
    responses={
        200: {"description": "Successfully got cars from database"},
        502: {"description": "Database error"},
        500: {"description": "Unknown error"},
    },
)
async def get_cars_list_view(
    response: Response,
    offset: int = Query(ge=0),
    limit: int = Query(ge=0),
    pool=Depends(get_connection_pool),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    cars_list, count = await get_cars_list(pool, offset, limit)
    response.status_code = 200  # type: ignore
    return {"records": cars_list, "total": count}


@cars_router.delete(
    "/{id}",
    responses={
        204: {"description": "Successfully deleted car from database"},
        404: {"description": "Car not found"},
        502: {"description": "Database error"},
        500: {"description": "Unknown error"},
    },
)
async def delete_car_view(
    response: Response,
    car_id: int = Query(ge=0),
    pool=Depends(get_connection_pool),
    current_user: User = Depends(get_current_active_user),
):
    await delete_car(pool, car_id)
    response.status_code = 204  # type: ignore
    return
