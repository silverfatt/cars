from functools import wraps

from asyncpg import Pool
from fastapi.exceptions import HTTPException
from loguru import logger

from ...api.v1.cars.models import Car, CollectedCar


def db_wrapper(func):
    async def inner(*args, **kwargs):

        try:
            await func(*args, **kwargs)
        except Exception as e:
            logger.error(
                f'msg="Unknown error during database operations", error="{repr(e)}"'
            )
            raise HTTPException(status_code=502, detail="Database issue")

    return inner


@db_wrapper
async def add_car_to_db(pool: Pool, car_to_create: Car):
    query = f"""
            INSERT INTO car ({", ".join(car_to_create.model_dump(exclude_none=True).keys())})
            VALUES ({", ".join([f"${i+1}" for i in range(len(car_to_create.model_dump(exclude_none=True).keys()))])})
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(
                query, *car_to_create.model_dump(exclude_none=True).values()
            )
