from asyncpg import Pool

from ....external.postgres.utils import add_car_to_db
from .models import Car


async def add_car(pool: Pool, car_to_add: Car):
    created_id = await add_car_to_db(pool, car_to_add)
    return created_id
