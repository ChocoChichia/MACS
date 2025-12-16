from fastapi import APIRouter, HTTPException, status

from core.habit import LoggableHabit
from infra.api.converters import (
    log_to_domain,
    log_to_response,
    stat_to_response,
    to_response,
)
from infra.api.dependencies import HabitRepoDep, LogRepoDep
from infra.api.schemas.habit import HabitRead
from infra.api.schemas.log import LogCreate, LogRead
from infra.api.schemas.stat import StatisticsRead

router = APIRouter()


@router.post(
    "/{habit_id}/logs",
    response_model=HabitRead,
    status_code=status.HTTP_201_CREATED,
)
def add_log(
    habit_id: str,
    request: LogCreate,
    habit_repo: HabitRepoDep,
    log_repo: LogRepoDep,
) -> HabitRead:
    habit = habit_repo.get_by_id(habit_id)

    if not isinstance(habit, LoggableHabit):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Cannot add logs to a Routine directly.",
        )

    log = log_to_domain(request, habit.type)
    log_repo.add_log(habit_id, log)

    updated_habit = habit_repo.get_by_id(habit_id)
    return to_response(updated_habit)


@router.get(
    "/{habit_id}/logs",
    response_model=list[LogRead],
)
def list_logs(
    habit_id: str,
    log_repo: LogRepoDep,
) -> list[LogRead]:
    logs = log_repo.get_logs(habit_id)
    return [log_to_response(log) for log in logs]


@router.get(
    "/{habit_id}/stats",
    response_model=StatisticsRead,
)
def get_stats(
    habit_id: str,
    habit_repo: HabitRepoDep,
) -> StatisticsRead:
    habit = habit_repo.get_by_id(habit_id)

    return stat_to_response(habit.get_statistics())
