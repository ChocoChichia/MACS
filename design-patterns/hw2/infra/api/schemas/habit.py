from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class HabitBase(BaseModel):
    name: str
    description: str
    category: str


class CreateBooleanHabit(HabitBase):
    type: Literal["boolean"]


class CreateNumericHabit(HabitBase):
    type: Literal["numeric"]
    goal: float = Field(gt=0, description="Target value for the habit")


class CreateRoutine(HabitBase):
    type: Literal["routine"]


class HabitReadBase(HabitBase):
    id: str
    model_config = ConfigDict(from_attributes=True)


class BooleanHabitRead(HabitReadBase):
    type: Literal["boolean"] = "boolean"


class NumericHabitRead(HabitReadBase):
    type: Literal["numeric"] = "numeric"
    goal: float


class RoutineRead(HabitReadBase):
    type: Literal["routine"] = "routine"
    subhabit_count: int = 0


class AddSubHabitRequest(BaseModel):
    subhabit_id: str


HabitRead = Annotated[
    BooleanHabitRead | NumericHabitRead | RoutineRead,
    Field(discriminator="type"),
]

CreateHabitRequest = Annotated[
    CreateBooleanHabit | CreateNumericHabit | CreateRoutine,
    Field(discriminator="type"),
]
