from datetime import date

import pytest

from core.logs import BooleanLog, NumericLog
from core.stats import (
    AverageCalculator,
    BooleanGoal,
    CompletionCalculator,
    NumericGoal,
    StandardDailyProgress,
    Statistics,
)


class MockTimeProvider:
    def __init__(self, current_date: date) -> None:
        self._current_date = current_date

    def today(self) -> date:
        return self._current_date


class TestStandardDailyProgress:
    def test_calculate_daily_progress_boolean(self) -> None:
        progress = StandardDailyProgress().calculate_daily_progress(
            BooleanLog(date=date(2025, 1, 1), completed=True), BooleanGoal()
        )
        assert progress == 1.0

    def test_calculate_daily_progress_numeric(self) -> None:
        progress = StandardDailyProgress().calculate_daily_progress(
            NumericLog(date=date(2025, 1, 1), value=5.0), NumericGoal(target=10.0)
        )
        assert progress == 0.5

    def test_is_completed_boolean_true(self) -> None:
        assert (
            StandardDailyProgress().is_completed(
                BooleanLog(date=date(2025, 1, 1), completed=True), BooleanGoal()
            )
            is True
        )

    def test_is_completed_boolean_false(self) -> None:
        assert (
            StandardDailyProgress().is_completed(
                BooleanLog(date=date(2025, 1, 1), completed=False), BooleanGoal()
            )
            is False
        )

    def test_is_completed_numeric_met(self) -> None:
        assert (
            StandardDailyProgress().is_completed(
                NumericLog(date=date(2025, 1, 1), value=10.0), NumericGoal(target=10.0)
            )
            is True
        )

    def test_is_completed_numeric_not_met(self) -> None:
        assert (
            StandardDailyProgress().is_completed(
                NumericLog(date=date(2025, 1, 1), value=5.0), NumericGoal(target=10.0)
            )
            is False
        )


class TestCompletionCalculator:
    def test_zero_completions_with_empty_logs(self) -> None:
        assert (
            CompletionCalculator().calculate_total_completions(
                [], StandardDailyProgress(), BooleanGoal()
            )
            == 0
        )

    def test_counts_all_completed_boolean_logs(self) -> None:
        logs = [
            BooleanLog(date=date(2025, 1, 1), completed=True),
            BooleanLog(date=date(2025, 1, 2), completed=False),
            BooleanLog(date=date(2025, 1, 3), completed=True),
        ]
        assert (
            CompletionCalculator().calculate_total_completions(
                logs, StandardDailyProgress(), BooleanGoal()
            )
            == 2
        )

    def test_counts_completed_numeric_goals(self) -> None:
        logs = [
            NumericLog(date=date(2025, 1, 1), value=10.0),
            NumericLog(date=date(2025, 1, 2), value=5.0),
            NumericLog(date=date(2025, 1, 3), value=15.0),
        ]
        assert (
            CompletionCalculator().calculate_total_completions(
                logs, StandardDailyProgress(), NumericGoal(target=10.0)
            )
            == 2
        )


class TestAverageCalculator:
    def test_zero_average_with_empty_logs(self) -> None:
        assert (
            AverageCalculator().calculate_average_progress(
                [], StandardDailyProgress(), BooleanGoal()
            )
            == 0.0
        )

    def test_average_with_boolean_logs(self) -> None:
        logs = [
            BooleanLog(date=date(2025, 1, 1), completed=True),
            BooleanLog(date=date(2025, 1, 2), completed=False),
            BooleanLog(date=date(2025, 1, 3), completed=True),
        ]
        assert AverageCalculator().calculate_average_progress(
            logs, StandardDailyProgress(), BooleanGoal()
        ) == pytest.approx(2.0 / 3.0)

    def test_average_with_numeric_logs(self) -> None:
        logs = [
            NumericLog(date=date(2025, 1, 1), value=10.0),
            NumericLog(date=date(2025, 1, 2), value=5.0),
            NumericLog(date=date(2025, 1, 3), value=20.0),
        ]
        assert AverageCalculator().calculate_average_progress(
            logs, StandardDailyProgress(), NumericGoal(target=10.0)
        ) == pytest.approx(2.5 / 3.0)


class TestStatistics:
    def test_statistics_creation(self) -> None:
        stats = Statistics(
            total_completions=10, current_streak=5, average_progress=0.85
        )
        assert stats.total_completions == 10
        assert stats.current_streak == 5
        assert stats.average_progress == 0.85

    def test_statistics_equality(self) -> None:
        s1 = Statistics(total_completions=10, current_streak=5, average_progress=0.85)
        s2 = Statistics(total_completions=10, current_streak=5, average_progress=0.85)
        assert s1 == s2
