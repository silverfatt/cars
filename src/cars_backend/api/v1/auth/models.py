from typing import Optional, Union

from pydantic import BaseModel, constr


class User(BaseModel):
    initials: str
    position: str
    phone: str  # constr(strip_whitespace=True, regex=r"7\d{10}")  # type: ignore
    email: str  # type: ignore
    disabled: Union[bool, None] = None
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None


class UserInDB(User):
    hashed_password: str
