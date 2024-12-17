from asyncpg import Pool

from ....external.postgres.utils_trip import (
    add_trip_to_db,
    delete_trip_from_db,
    get_trip_from_db,
    get_trips_list_from_db,
)

from .models import Trip, CollectedTrip

async def add_trip(pool: Pool, driver_to_add: Trip):
    created_id = await add_trip_to_db(pool, driver_to_add)
    return created_id

async def get_trip(pool: Pool, trip_id: int) -> CollectedTrip:
    trip = await get_trip_from_db(pool, trip_id)
    return trip

async def get_trips_list(pool: Pool, offest: int, limit: int) -> list[CollectedTrip]:
    trip_list = await get_trips_list_from_db (pool, offest, limit)
    return trip_list

async def delete_trip(pool: Pool, trip_id: int) -> None:
    await delete_trip_from_db(pool, trip_id)
