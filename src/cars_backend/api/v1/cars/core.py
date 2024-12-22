from asyncpg import Pool

from ....external.postgres.utils import (
    add_car_to_db,
    count_records_in_table,
    delete_car_from_db,
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


async def get_cars_list(
    pool: Pool, offset: int, limit: int
) -> tuple[list[CollectedCar], int]:
    cars_list = await get_cars_list_from_db(pool, offset, limit)
    total_cars = await count_records_in_table(pool, "car")
    return cars_list, total_cars


async def delete_car(pool: Pool, car_id: int) -> None:
    await delete_car_from_db(pool, car_id)
