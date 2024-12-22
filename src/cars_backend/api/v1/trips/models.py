from datetime import date
from pydantic import BaseModel, field_validator


class Trip(BaseModel):
    trip_date: date
    distance_km: float
    rating: int
    cost: float
    driver_id: int

    @field_validator("trip_date")
    @classmethod
    def check_trip_date(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("trip date cannot be in the future")
        return v

    @field_validator("distance_km")
    @classmethod
    def check_distance_km(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("distance must be a positive number")
        return v

    @field_validator("rating")
    @classmethod
    def check_rating(cls, v: int) -> int:
        if v < 1 or v > 5:
            raise ValueError("rating must be between 1 and 5")
        return v

    @field_validator("cost")
    @classmethod
    def check_cost(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("cost must be positive")
        return v


class CollectedTrip(Trip):
    id: int
