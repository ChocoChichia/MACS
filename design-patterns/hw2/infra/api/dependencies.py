from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from core.habit import HabitFactory, StandardHabitFactory
from core.logs import SystemTimeProvider
from core.repository import HabitRepository, LogRepository
from infra.persistance.in_memory import InMemoryHabitRepository, InMemoryLogRepository


@lru_cache
def get_habit_repository() -> InMemoryHabitRepository:
    return InMemoryHabitRepository()


def get_log_repository() -> LogRepository:
    habit_repo = get_habit_repository()
    return InMemoryLogRepository(habit_repo)


def get_habit_factory() -> HabitFactory:
    return StandardHabitFactory(SystemTimeProvider())


HabitRepoDep = Annotated[HabitRepository, Depends(get_habit_repository)]
LogRepoDep = Annotated[LogRepository, Depends(get_log_repository)]
FactoryDep = Annotated[HabitFactory, Depends(get_habit_factory)]
