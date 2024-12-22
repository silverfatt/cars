from datetime import datetime, timedelta

import numpy as np
from asyncpg import Pool
from fastapi import Query, Response
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from pydantic import BaseModel

from ....external.ml_model.upload_model import model
from ....external.postgres.connection import get_connection_pool
from ..auth.auth import get_current_active_user
from ..auth.models import User
from .core import predict_next_maintenance

dashboards_router = APIRouter(prefix="/api/v1/dashboards", tags=["dashboards"])


@dashboards_router.get(
    "/predict",
    responses={
        200: {"description": "Successfully predicted"},
        404: {"description": "Car not found"},
    },
)
async def predict_next_maintenance_view(
    car_id: int,
    response: Response,
    pool: Pool = Depends(get_connection_pool),
    current_user: User = Depends(get_current_active_user),
):
    recommended_date = await predict_next_maintenance(pool, car_id, model)
    response.status_code = 200  # type: ignore
    return {"recommended_to_date": recommended_date}
