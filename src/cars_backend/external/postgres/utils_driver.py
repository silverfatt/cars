from functools import wraps

from asyncpg import Pool
from fastapi.exceptions import HTTPException
from loguru import logger

from ...api.v1.drivers.models import Driver, CollectedDriver
from .exceptions import NotFoundException

def db_wrapper(func):
    async def inner(*args, **kwargs):

        try:
            return await func(*args, **kwargs)
        except NotFoundException as e:
            logger.error(f'msg="Driver not found", error="{repr(e)}"')
            raise HTTPException(status_code=404, detail="Not Found")
        except Exception as e:
            logger.error(
                f'msg="Unknown error during database operations", error="{repr(e)}"'
            )
            raise HTTPException(status_code=502, detail="Database issue")

    return inner


@db_wrapper
async def add_driver_to_db(pool: Pool, driver_to_create: Driver):
    query = f"""
            INSERT INTO driver ({", ".join(driver_to_create.model_dump(exclude_none=True).keys())})
            VALUES ({", ".join([f"${i+1}" for i in range(len(driver_to_create.model_dump(exclude_none=True).keys()))])})
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(
                query, *driver_to_create.model_dump(exclude_none=True).values()
            )

@db_wrapper
async def get_driver_from_db(pool: Pool, driver_id: int) -> CollectedDriver:
    query = f"""
            SELECT * FROM driver
            WHERE id = $1
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetchrow(query, driver_id)
    if not res:
        raise NotFoundException("Driver not found")
    return CollectedDriver(**res)


@db_wrapper
async def get_drivers_list_from_db(
    pool: Pool, offset: int, limit: int
) -> list[CollectedDriver]:
    query = """
            SELECT * FROM driver
            ORDER BY id ASC
            OFFSET $1
            LIMIT $2
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetch(query, offset, limit)
    return [CollectedDriver(**row) for row in res]


@db_wrapper
async def delete_driver_from_db(pool: Pool, driver_id: int):
    query = f"""
            DELETE FROM driver
            WHERE id = $1
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            res = await connection.execute(query, driver_id)
            print(res)
    if int(res.split()[1]) == 0:
        raise NotFoundException("Driver not found")
    return

