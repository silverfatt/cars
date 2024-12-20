from fastapi import Query, Response
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter

from ....external.postgres.connection import get_connection_pool
from ..auth.auth import get_current_active_user
from ..auth.models import User
from .core import add_trip, delete_trip, get_trip, get_trips_list_from_db
from .models import CollectedTrip, Trip

trips_router = APIRouter(prefix="/api/v1/trip", tags=["trips"])


@trips_router.post(
    "/",
    responses={
        201: {"description": "Added new trip to database"},
        502: {"description": "Database error"},
        500: {"description": "Unknown error"},
    },
)
async def add_trip_view(
    trips_to_add: Trip,
    response: Response,
    pool=Depends(get_connection_pool),
    current_user: User = Depends(get_current_active_user),
) -> str:
    await add_trip(pool, trips_to_add)
    response.status_code = 201
    return "ok"


@trips_router.get(
    "/{id}",
    responses={
        200: {"description": "Successfully got trip from database"},
        404: {"description": "Trip not found"},
        502: {"description": "Database error"},
        500: {"description": "Unknown error"},
    },
)
async def get_trip_view(
    response: Response,
    trip_id: int = Query(ge=0),
    pool=Depends(get_connection_pool),
    current_user: User = Depends(get_current_active_user),
) -> CollectedTrip:
    trip = await get_trip(pool, trip_id)
    response.status_code = 200
    return trip


@trips_router.get(
    "/",
    responses={
        200: {"description": "Successfully got trips from database"},
        502: {"description": "Database error"},
        500: {"description": "Unknown error"},
    },
)
async def get_trips_list(
    response: Response,
    offset: int = Query(ge=0),
    limit: int = Query(ge=0),
    pool=Depends(get_connection_pool),
    current_user: User = Depends(get_current_active_user),
) -> list[CollectedTrip]:
    trips_list = await get_trips_list_from_db(pool, offset, limit)
    response.status_code = 200
    return trips_list


@trips_router.delete(
    "/{id}",
    responses={
        204: {"description": "Successfully deleted trip from database"},
        404: {"description": "Driver not found"},
        501: {"description": "Database error"},
        500: {"description": "Unknown error"},
    },
)
async def delete_trip_view(
    response: Response,
    trip_id: int = Query(ge=0),
    pool=Depends(get_connection_pool),
    current_user: User = Depends(get_current_active_user),
):
    await delete_trip(pool, trip_id)
    response.status_code = 204
    return
