from functools import wraps

from asyncpg import Pool
from fastapi.exceptions import HTTPException
from loguru import logger

from ...api.v1.trip.models import Trip, CollectedTrip
from .exceptions import NotFoundException

def db_wrapper(func):
    async def inner(*args, **kwargs):

        try:
            return await func(*args, **kwargs)
        except NotFoundException as e:
            logger.error(f'msg="Car not found", error="{repr(e)}"')
            raise HTTPException(status_code=404, detail="Not Found")
        except Exception as e:
            logger.error(
                f'msg="Unknown error during database operations", error="{repr(e)}"'
            )
            raise HTTPException(status_code=502, detail="Database issue")

    return inner


@db_wrapper
async def add_trip_to_db(pool: Pool, trip_to_create: Trip):
    query = f"""
            INSERT INTO car ({", ".join(trip_to_create.model_dump(exclude_none=True).keys())})
            VALUES ({", ".join([f"${i+1}" for i in range(len(trip_to_create.model_dump(exclude_none=True).keys()))])})
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(
                query, *trip_to_create.model_dump(exclude_none=True).values()
            )

@db_wrapper
async def get_trip_from_db(pool: Pool, trip_id: int) -> CollectedTrip:
    query = f"""
            SELECT * FROM trip
            WHERE id = $1
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetchrow(query, trip_id)
    if not res:
        raise NotFoundException("Trip not found")
    return CollectedTrip(**res)


@db_wrapper
async def get_trips_list_from_db(
    pool: Pool, offset: int, limit: int
) -> list[CollectedTrip]:
    query = """
            SELECT * FROM trip
            ORDER BY id ASC
            OFFSET $1
            LIMIT $2
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetch(query, offset, limit)
    return [CollectedTrip(**row) for row in res]


@db_wrapper
async def delete_trip_from_db(pool: Pool, trip_id: int):
    query = f"""
            DELETE FROM trip
            WHERE id = $1
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            res = await connection.execute(query, trip_id)
            print(res)
    if int(res.split()[1]) == 0:
        raise NotFoundException("Trip not found")
    return

