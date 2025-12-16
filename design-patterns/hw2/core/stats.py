from collections.abc import Sequence
from dataclasses import dataclass
from datetime import timedelta
from typing import Protocol

from core.logs import Log, TimeProvider


@dataclass
class Statistics:
    """Aggregated statistics for a habit."""

    total_completions: int
    current_streak: int
    average_progress: float


class Goal(Protocol):
    """Protocol for habit goals."""

    def is_achieved(self, value: float) -> bool:
        """Check if the goal is achieved for a given value."""
        ...

    def calculate_progress(self, value: float) -> float:
        """Calculate progress toward the goal (0.0 to 1.0)."""
        ...


@dataclass(frozen=True)
class BooleanGoal:
    target: bool = True

    def is_achieved(self, value: float) -> bool:
        return value >= 1.0

    def calculate_progress(self, value: float) -> float:
        return 1.0 if value >= 1.0 else 0.0


@dataclass(frozen=True)
class NumericGoal:
    target: float

    def is_achieved(self, value: float) -> bool:
        return value >= self.target

    def calculate_progress(self, value: float) -> float:
        if self.target <= 0:
            return 0.0
        return min(value / self.target, 1.0)


class DailyProgress(Protocol):
    """Protocol for calculating daily progress based on logs."""

    def calculate_daily_progress(self, log: Log, goal: Goal) -> float:
        """Calculate progress for a single log entry."""
        ...

    def is_completed(self, log: Log, goal: Goal) -> bool:
        """Check if the log represents a completed day."""
        ...


class StandardDailyProgress:
    def calculate_daily_progress(self, log: Log, goal: Goal) -> float:
        return goal.calculate_progress(log.get_value())

    def is_completed(self, log: Log, goal: Goal) -> bool:
        return goal.is_achieved(log.get_value())


class StreakCalculator:
    def __init__(self, time_provider: TimeProvider) -> None:
        self.time_provider = time_provider

    def calculate_current_streak(
        self, logs: Sequence[Log], strategy: DailyProgress, goal: Goal
    ) -> int:
        if not logs:
            return 0

        completed_dates = {log.date for log in logs if strategy.is_completed(log, goal)}

        today = self.time_provider.today()

        start_day = today if today in completed_dates else today - timedelta(days=1)

        streak = 0
        day = start_day

        while day in completed_dates:
            streak += 1
            day -= timedelta(days=1)

        return streak


class CompletionCalculator:
    """Calculates total number of completions."""

    def calculate_total_completions(
        self, logs: Sequence[Log], strategy: DailyProgress, goal: Goal
    ) -> int:
        return sum(1 for log in logs if strategy.is_completed(log, goal))


class AverageCalculator:
    """Calculates average progress across all logs."""

    def calculate_average_progress(
        self, logs: Sequence[Log], strategy: DailyProgress, goal: Goal
    ) -> float:
        if not logs:
            return 0.0
        total = sum(strategy.calculate_daily_progress(log, goal) for log in logs)
        return total / len(logs)


class StatisticsCalculator:
    """Aggregates various statistics calculations."""

    def __init__(self, strategy: DailyProgress, time_provider: TimeProvider) -> None:
        self.strategy = strategy
        self.streak_calculator = StreakCalculator(time_provider)
        self.completion_calculator = CompletionCalculator()
        self.average_calculator = AverageCalculator()

    def calculate_average_progress(self, logs: Sequence[Log], goal: Goal) -> float:
        return self.average_calculator.calculate_average_progress(
            logs, self.strategy, goal
        )

    def calculate_statistics(self, logs: Sequence[Log], goal: Goal) -> Statistics:
        total = self.completion_calculator.calculate_total_completions(
            logs, self.strategy, goal
        )
        streak = self.streak_calculator.calculate_current_streak(
            logs, self.strategy, goal
        )
        avg = self.calculate_average_progress(logs, goal)

        return Statistics(
            total_completions=total, current_streak=streak, average_progress=avg
        )
