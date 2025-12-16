from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

from core.logs import Log, TimeProvider
from core.stats import (
    BooleanGoal,
    Goal,
    NumericGoal,
    StandardDailyProgress,
    Statistics,
    StatisticsCalculator,
)


class HabitType(str, Enum):
    BOOLEAN = "boolean"
    NUMERIC = "numeric"
    ROUTINE = "routine"


@dataclass
class Habit(ABC):
    """Abstract base class for all habits."""

    id: str
    name: str
    description: str
    category: str
    type: HabitType

    @abstractmethod
    def get_progress(self) -> float:
        """Get the current progress of the habit (0.0 to 1.0)."""
        pass

    @abstractmethod
    def get_statistics(self) -> Statistics:
        """Get aggregated statistics for the habit."""
        pass


@dataclass
class LoggableHabit(Habit, ABC):
    @abstractmethod
    def add_log(self, log: Log) -> None:
        pass

    @abstractmethod
    def get_logs(self) -> list[Log]:
        pass


@dataclass
class SimpleHabit(LoggableHabit):
    """A simple habit with goal tracking and statistics."""

    goal: Goal
    calculator: StatisticsCalculator = field(compare=False)
    logs: list[Log] = field(default_factory=list)

    def add_log(self, log: Log) -> None:
        self.logs.append(log)

    def get_logs(self) -> list[Log]:
        return self.logs.copy()

    def get_progress(self) -> float:
        return self.calculator.calculate_average_progress(self.logs, self.goal)

    def get_statistics(self) -> Statistics:
        return self.calculator.calculate_statistics(self.logs, self.goal)


@dataclass
class Routine(Habit):
    """A composite habit consisting of multiple sub-habits."""

    habits: list[Habit] = field(default_factory=list)

    def add_habit(self, habit: Habit) -> None:
        self.habits.append(habit)

    def remove_habit(self, habit: Habit) -> None:
        self.habits.remove(habit)

    def get_progress(self) -> float:
        if not self.habits:
            return 0.0
        total = sum(h.get_progress() for h in self.habits)
        return total / len(self.habits)

    def get_statistics(self) -> Statistics:
        if not self.habits:
            return Statistics(
                total_completions=0, current_streak=0, average_progress=0.0
            )

        all_stats = [habit.get_statistics() for habit in self.habits]
        total_completions = sum(stat.total_completions for stat in all_stats)
        current_streak = min(stat.current_streak for stat in all_stats)
        average_progress = sum(stat.average_progress for stat in all_stats) / len(
            all_stats
        )

        return Statistics(
            total_completions=total_completions,
            current_streak=current_streak,
            average_progress=average_progress,
        )


class HabitFactory(ABC):
    """Abstract factory for creating habits."""

    @abstractmethod
    def create_boolean_habit(
        self, name: str, description: str, category: str
    ) -> SimpleHabit:
        pass

    @abstractmethod
    def create_numeric_habit(
        self, name: str, description: str, category: str, goal_value: float
    ) -> SimpleHabit:
        pass

    @abstractmethod
    def create_routine(self, name: str, description: str, category: str) -> Routine:
        pass


class StandardHabitFactory(HabitFactory):
    """Standard factory implementation for creating habits."""

    def __init__(self, time_provider: TimeProvider) -> None:
        self.time_provider = time_provider

    def create_boolean_habit(
        self, name: str, description: str, category: str
    ) -> SimpleHabit:
        return SimpleHabit(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            category=category,
            type=HabitType.BOOLEAN,
            goal=BooleanGoal(),
            calculator=StatisticsCalculator(
                StandardDailyProgress(), self.time_provider
            ),
        )

    def create_numeric_habit(
        self, name: str, description: str, category: str, goal_value: float
    ) -> SimpleHabit:
        return SimpleHabit(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            category=category,
            type=HabitType.NUMERIC,
            goal=NumericGoal(target=goal_value),
            calculator=StatisticsCalculator(
                StandardDailyProgress(), self.time_provider
            ),
        )

    def create_routine(self, name: str, description: str, category: str) -> Routine:
        return Routine(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            category=category,
            type=HabitType.ROUTINE,
        )
