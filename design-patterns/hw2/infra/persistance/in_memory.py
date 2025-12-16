import copy
from dataclasses import dataclass, field

from core.errors import HabitNotFoundError
from core.habit import Habit, LoggableHabit
from core.logs import Log
from core.repository import HabitRepository, LogRepository


@dataclass
class InMemoryHabitRepository(HabitRepository):
    items: dict[str, Habit] = field(default_factory=dict)

    def save(self, habit: Habit) -> None:
        self.items[habit.id] = copy.deepcopy(habit)

    def get_by_id(self, habit_id: str) -> Habit:
        if habit_id not in self.items:
            raise HabitNotFoundError(habit_id)

        return copy.deepcopy(self.items[habit_id])

    def list_all(self) -> list[Habit]:
        return [copy.deepcopy(habit) for habit in self.items.values()]

    def delete(self, habit_id: str) -> None:
        try:
            del self.items[habit_id]
        except KeyError:
            raise HabitNotFoundError(habit_id) from None


@dataclass
class InMemoryLogRepository(LogRepository):
    _habit_repo: InMemoryHabitRepository

    def add_log(self, habit_id: str, log: Log) -> None:
        habit = self._habit_repo.get_by_id(habit_id)

        if isinstance(habit, LoggableHabit):
            habit.add_log(log)
            self._habit_repo.save(habit)

    def get_logs(self, habit_id: str) -> list[Log]:
        habit = self._habit_repo.get_by_id(habit_id)

        if isinstance(habit, LoggableHabit):
            return habit.get_logs()

        return []
