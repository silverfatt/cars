from datetime import date
from typing import Optional

from pydantic import BaseModel, field_validator


class Car(BaseModel):
    model: str
    year_of_manufacture: int
    mileage: int
    last_maintenance_date: date
    recommended_maintenance_date: Optional[date] = None

    @field_validator("year_of_manufacture")
    @classmethod
    def value_must_be_real(cls, v: int) -> int:
        if v < 1950 or v > date.today().year:
            raise ValueError("value is unrealistic")
        return v

    @field_validator("last_maintenance_date")
    @classmethod
    def date_must_be_real(cls, v: date) -> date:
        if v.year < 1950 or v > date.today():
            raise ValueError("value is unrealistic")
        return v

    @field_validator("recommended_maintenance_date")
    @classmethod
    def date_must_be_real_if_exists(cls, v: date) -> date:
        if v and v.year < 1950:
            raise ValueError("value is unrealistic")
        return v

    @field_validator("mileage")
    def value_must_be_positive(cls, v: int) -> int:
        if v < 0:
            raise ValueError("valuemust be positive")
        return v


class CollectedCar(Car):
    id: int
