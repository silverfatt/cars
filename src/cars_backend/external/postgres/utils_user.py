from typing import Optional

from ...api.v1.auth.models import UserInDB
from .connection import get_connection_pool


async def get_user_from_db(email: str) -> Optional[UserInDB]:
    pool = get_connection_pool()
    query = """
            SELECT *
            FROM users WHERE email = $1
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            row = await connection.fetchrow(query, email)
            if not row:
                return None
            return UserInDB(
                password="",
                position=row["position"],
                initials=row["initials"],
                phone=row["phone"],
                email=row["email"],
                hashed_password=row["hashed_password"],
            )


async def get_user_id_from_db(email: str) -> Optional[int]:
    pool = get_connection_pool()
    query = """
            SELECT id
            FROM users WHERE email = $1
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            row = await connection.fetchrow(query, email)
            if not row:
                return None
            return row["id"]


async def create_user(new_user: UserInDB):
    pool = get_connection_pool()
    query = """
            INSERT INTO users (hashed_password, email, phone, initials, position)
            VALUES ($1, $2, $3, $4, $5)
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.fetch(
                query,
                new_user.hashed_password,
                new_user.email,
                new_user.phone,
                new_user.initials,
                new_user.position,
            )
