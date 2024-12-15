from asyncpg import Pool

from ....external.postgres.utils import (
    add_car_to_db,
    get_car_from_db,
    get_cars_list_from_db,
)
from .models import Car, CollectedCar


async def add_car(pool: Pool, car_to_add: Car):
    created_id = await add_car_to_db(pool, car_to_add)
    return created_id


async def get_car(pool: Pool, car_id: int) -> CollectedCar:
    car = await get_car_from_db(pool, car_id)
    return car


async def get_cars_list(pool: Pool, offset: int, limit: int) -> list[CollectedCar]:
    cars_list = await get_cars_list_from_db(pool, offset, limit)
    return cars_list
