from functools import wraps

from asyncpg import Pool
from fastapi.exceptions import HTTPException
from loguru import logger

from ...api.v1.auth.models import UserInDB
from ...api.v1.cars.models import Car, CollectedCar
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


@db_wrapper
async def get_car_from_db(pool: Pool, car_id: int) -> CollectedCar:
    query = f"""
            SELECT * FROM car
            WHERE id = $1
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetchrow(query, car_id)
    if not res:
        raise NotFoundException("Car not found")
    return CollectedCar(**res)


@db_wrapper
async def get_cars_list_from_db(
    pool: Pool, offset: int, limit: int
) -> list[CollectedCar]:
    query = """
            SELECT * FROM car
            ORDER BY id ASC
            OFFSET $1
            LIMIT $2
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetch(query, offset, limit)
    return [CollectedCar(**row) for row in res]


@db_wrapper
async def delete_car_from_db(pool: Pool, car_id: int):
    query = f"""
            DELETE FROM car
            WHERE id = $1
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            res = await connection.execute(query, car_id)
            print(res)
    if int(res.split()[1]) == 0:
        raise NotFoundException("Car not found")
    return


@db_wrapper
async def count_records_in_table(pool: Pool, table_name: str) -> int:
    query = f"SELECT COUNT(*) FROM {table_name}"  # Не является уязвимостью к SQL инъекциям, т к названия таблиц захардкожены в core.py файлах
    async with pool.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetchval(query)
    return res
