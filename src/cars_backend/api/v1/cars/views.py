from fastapi import Response
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter

from ....external.postgres.connection import get_connection_pool

cars_router = APIRouter(prefix="/api/v1/cars", tags=["cars"])


@cars_router.get("/api/v1/cars")
async def test_route() -> str:
    return "ok"
