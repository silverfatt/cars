from datetime import date, datetime, timedelta

import numpy as np
from asyncpg import Pool
from loguru import logger

from ....external.ml_model.upload_model import Model
from ....external.postgres.utils import (
    get_car_from_db,
    update_car_recommended_maintenance,
)


async def predict_next_maintenance(pool: Pool, car_id: int, model: Model) -> str:
    car = await get_car_from_db(pool, car_id)
    if (
        car.recommended_maintenance_date
        and car.recommended_maintenance_date >= date.today()
    ):
        logger.debug(
            f'msg="Recommended date for car_id is already predicted" car_id={car_id}'
        )
        return car.recommended_maintenance_date.isoformat()
    input_data = np.array([[car.year_of_manufacture, car.mileage]])

    predicted_days = model.predictor.predict(input_data)[0]

    current_date = datetime.now()
    recommended_date = current_date + timedelta(days=int(predicted_days))
    await update_car_recommended_maintenance(pool, car_id, recommended_date)
    return recommended_date.date().isoformat()
