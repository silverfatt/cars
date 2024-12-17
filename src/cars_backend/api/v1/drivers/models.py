from pydantic import BaseModel, field_validator


class Driver(BaseModel):
    name: str
    experience_years: int
    car_id: int
    violations: int


    @field_validator("experitnce_years")
    @classmethod

    def check_experience_years(cls, v: int) -> int:
        if v < 0:
            raise ValueError("experience years must be positive")
        return v

class CollectedDriver(Driver):
    id: int