from datetime import datetime, timedelta

import numpy as np
from fastapi import Query, Response
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from pydantic import BaseModel

from ....external.ml_model.upload_model import model
from ....external.postgres.connection import get_connection_pool
from ..auth.auth import get_current_active_user
from ..auth.models import User

dashboards_router = APIRouter(prefix="/api/v1/dashboards", tags=["dashboards"])


@dashboards_router.get(
    "/",
    responses={
        200: {"description": "Successfully predicted"},
    },
)
async def predict_car(
    response: Response,
    current_user: User = Depends(get_current_active_user),
) -> str:
    return "ok"


class UserData(BaseModel):
    year_of_manufacture: int
    mileage: int
    last_maintenance_date: str


@dashboards_router.post("/predict/")
async def predict_next_maintenance(user_data: UserData):
    # Преобразование входных данных в формат, который подходит для модели
    input_data = np.array([[user_data.year_of_manufacture, user_data.mileage]])

    # Получение прогноза
    predicted_days = model.predictor.predict(input_data)[0]

    # Получаем текущую дату и вычисляем рекомендуемую дату ТО
    current_date = datetime.now()
    recommended_date = current_date + timedelta(days=int(predicted_days))

    # Возвращаем предсказанную дату ТО
    return {"recommended_to_date": recommended_date.date().isoformat()}
