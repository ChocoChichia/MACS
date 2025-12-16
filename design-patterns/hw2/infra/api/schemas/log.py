from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class LogBase(BaseModel):
    date: date


class LogCreate(LogBase):
    value: float


class LogReadBase(LogBase):
    model_config = ConfigDict(from_attributes=True)


class BooleanLogRead(LogReadBase):
    type: Literal["boolean"] = "boolean"
    completed: bool


class NumericLogRead(LogReadBase):
    type: Literal["numeric"] = "numeric"
    value: float


LogRead = Annotated[
    BooleanLogRead | NumericLogRead,
    Field(discriminator="type"),
]
