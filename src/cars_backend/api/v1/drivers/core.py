from asyncpg import Pool

from ....external.postgres.utils_driver import (
    add_driver_to_db,
    delete_driver_from_db,
    get_driver_from_db,
    get_drivers_list_from_db,
)

from .models import Driver, CollectedDriver

async def add_driver(pool: Pool, driver_to_add: Driver):
    created_id = await add_driver_to_db(pool, driver_to_add)
    return created_id

async def get_driver(pool: Pool, driver_id: int) -> CollectedDriver:
    driver = await get_driver_from_db(pool, driver_id)
    return driver

async def get_drivers_list(pool: Pool, offest: int, limit: int) -> list[CollectedDriver]:
    driver_list = await get_drivers_list_from_db (pool, offest, limit)
    return driver_list

async def delete_driver(pool: Pool, driver_id: int) -> None:
    await delete_driver_from_db(pool, driver_id)
