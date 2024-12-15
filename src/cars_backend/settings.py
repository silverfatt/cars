from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    postgres_database: str
    loguru_level: Literal["INFO", "DEBUG"] = "DEBUG"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # type: ignore