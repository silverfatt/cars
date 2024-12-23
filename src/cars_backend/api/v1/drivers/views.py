from fastapi import Query, Response
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from loguru import logger

from ....external.postgres.connection import get_connection_pool
from ..auth.auth import get_current_active_user
from ..auth.models import User
from .core import add_driver, delete_driver, get_driver, get_drivers_list
from .models import CollectedDriver, Driver

drivers_router = APIRouter(prefix="/api/v1/driver", tags=["drivers"])


@drivers_router.post(
    "/",
    responses={
        201: {"description": "Added new driver to database"},
        502: {"description": "Database error"},
        500: {"description": "Unknown error"},
    },
)
async def add_driver_view(
    driver_to_add: Driver,
    response: Response,
    pool=Depends(get_connection_pool),
    current_user: User = Depends(get_current_active_user),
) -> str:
    await add_driver(pool, driver_to_add)
    response.status_code = 201
    return "ok"


@drivers_router.get(
    "/{id}",
    responses={
        200: {"description": "Successfully got driver from database"},
        404: {"description": "Driver not found"},
        502: {"description": "Database error"},
        500: {"description": "Unknown error"},
    },
)
async def get_driver_view(
    response: Response,
    driver_id: int = Query(ge=0),
    pool=Depends(get_connection_pool),
    current_user: User = Depends(get_current_active_user),
) -> CollectedDriver:
    driver = await get_driver(pool, driver_id)
    response.status_code = 200
    return driver


@drivers_router.get(
    "/",
    responses={
        200: {"description": "Successfully got drivers from database"},
        502: {"description": "Database error"},
        500: {"description": "Unknown error"},
    },
)
async def get_drivers_list_view(
    response: Response,
    offset: int = Query(ge=0),
    limit: int = Query(ge=0),
    pool=Depends(get_connection_pool),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    drivers_list, count = await get_drivers_list(pool, offset, limit)
    response.status_code = 200
    return {"records": drivers_list, "total": count}


@drivers_router.delete(
    "/{id}",
    responses={
        204: {"description": "Successfully deleted driver from database"},
        404: {"description": "Driver not found"},
        501: {"description": "Database error"},
        500: {"description": "Unknown error"},
    },
)
async def delete_driver_view(
    response: Response,
    driver_id: int = Query(ge=0),
    pool=Depends(get_connection_pool),
    current_user: User = Depends(get_current_active_user),
):
    await delete_driver(pool, driver_id)
    response.status_code = 204
    return
