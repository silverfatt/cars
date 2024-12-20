import os
import sys

from fastapi.applications import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from .api.ping import status_router
from .api.v1.auth.views import auth_router
from .api.v1.cars.views import cars_router
from .api.v1.dashboards.views import dashboards_router
from .api.v1.drivers.views import drivers_router
from .api.v1.trips.views import trips_router
from .external.ml_model.upload_model import load_model
from .external.postgres.connection import connect_postgres, disconnect_postgres
from .settings import settings

app = FastAPI(
    title="Phone Processing Service",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    version=os.getenv("APP_VERSION", default="DEV"),
)


logger_handlers = [
    {
        "sink": sys.stdout,
        "level": settings.loguru_level,
        "format": "<level>level={level} {message}</level>",
    }
]


def create_app():
    logger.configure(handlers=logger_handlers)  # type: ignore
    app.include_router(status_router)
    app.include_router(cars_router)
    app.include_router(drivers_router)
    app.include_router(trips_router)
    app.include_router(auth_router)
    app.include_router(dashboards_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", connect_postgres)
    app.add_event_handler("startup", load_model)
    app.add_event_handler("shutdown", disconnect_postgres)
    return app
