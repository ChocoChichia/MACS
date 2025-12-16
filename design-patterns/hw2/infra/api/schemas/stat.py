from pydantic import BaseModel, ConfigDict


class StatisticsRead(BaseModel):
    total_completions: int
    current_streak: int
    average_progress: float

    model_config = ConfigDict(from_attributes=True)
