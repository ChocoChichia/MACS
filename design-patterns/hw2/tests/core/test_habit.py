from datetime import date

import pytest

from core.habit import Habit, Routine, SimpleHabit, StandardHabitFactory
from core.logs import BooleanLog, NumericLog, SystemTimeProvider
from core.stats import BooleanGoal, Statistics


class MockTimeProvider:
    def __init__(self, current_date: date) -> None:
        self._current_date = current_date

    def today(self) -> date:
        return self._current_date


class TestSimpleHabit:
    def test_create_simple_habit(self) -> None:
        time_provider = SystemTimeProvider()
        factory = StandardHabitFactory(time_provider)
        habit = factory.create_boolean_habit("Exercise", "Daily workout", "Health")
        assert isinstance(habit, SimpleHabit)
        assert habit.name == "Exercise"
        assert habit.category == "Health"
        assert isinstance(habit.goal, BooleanGoal)
        assert habit.id != ""

    def test_add_log_to_habit(self) -> None:
        time_provider = SystemTimeProvider()
        factory = StandardHabitFactory(time_provider)
        habit = factory.create_boolean_habit("Exercise", "Daily", "Health")
        log = BooleanLog(date=date(2025, 1, 1), completed=True)
        habit.add_log(log)
        logs = habit.get_logs()
        assert len(logs) == 1
        assert logs[0] == log

    def test_get_logs_returns_copy(self) -> None:
        time_provider = SystemTimeProvider()
        factory = StandardHabitFactory(time_provider)
        habit = factory.create_boolean_habit("Exercise", "Daily", "Health")
        log = BooleanLog(date=date(2025, 1, 1), completed=True)
        habit.add_log(log)
        logs = habit.get_logs()
        logs.append(BooleanLog(date=date(2025, 1, 2), completed=True))
        assert len(habit.get_logs()) == 1

    def test_get_progress_with_no_logs(self) -> None:
        time_provider = SystemTimeProvider()
        factory = StandardHabitFactory(time_provider)
        habit = factory.create_boolean_habit("Exercise", "Daily", "Health")
        progress = habit.get_progress()
        assert progress == 0.0

    def test_get_progress_with_boolean_logs(self) -> None:
        time_provider = SystemTimeProvider()
        factory = StandardHabitFactory(time_provider)
        habit = factory.create_boolean_habit("Exercise", "Daily", "Health")
        habit.add_log(BooleanLog(date=date(2025, 1, 1), completed=True))
        habit.add_log(BooleanLog(date=date(2025, 1, 2), completed=False))
        habit.add_log(BooleanLog(date=date(2025, 1, 3), completed=True))
        progress = habit.get_progress()
        assert progress == pytest.approx(2.0 / 3.0)

    def test_get_progress_with_numeric_logs(self) -> None:
        time_provider = SystemTimeProvider()
        factory = StandardHabitFactory(time_provider)
        habit = factory.create_numeric_habit("Water", "8 glasses", "Health", 8.0)
        habit.add_log(NumericLog(date=date(2025, 1, 1), value=8.0))
        habit.add_log(NumericLog(date=date(2025, 1, 2), value=4.0))
        progress = habit.get_progress()
        assert progress == pytest.approx(0.75)

    def test_get_statistics(self) -> None:
        today = date(2025, 1, 5)
        time_provider = MockTimeProvider(today)
        factory = StandardHabitFactory(time_provider)
        habit = factory.create_boolean_habit("Exercise", "Daily", "Health")
        habit.add_log(BooleanLog(date=date(2025, 1, 1), completed=True))
        habit.add_log(BooleanLog(date=date(2025, 1, 2), completed=True))
        habit.add_log(BooleanLog(date=date(2025, 1, 3), completed=False))
        habit.add_log(BooleanLog(date=date(2025, 1, 4), completed=True))
        stats = habit.get_statistics()
        assert isinstance(stats, Statistics)
        assert stats.total_completions == 3
        assert stats.current_streak == 1
        assert stats.average_progress == 0.75

    def test_multiple_logs_same_date_allowed(self) -> None:
        time_provider = SystemTimeProvider()
        factory = StandardHabitFactory(time_provider)
        habit = factory.create_boolean_habit("Exercise", "Daily", "Health")
        habit.add_log(BooleanLog(date=date(2025, 1, 1), completed=True))
        habit.add_log(BooleanLog(date=date(2025, 1, 1), completed=False))
        assert len(habit.get_logs()) == 2


class TestRoutine:
    def test_create_routine(self) -> None:
        time_provider = SystemTimeProvider()
        factory = StandardHabitFactory(time_provider)
        routine = factory.create_routine("Morning Routine", "Start day", "Health")
        assert isinstance(routine, Routine)
        assert routine.name == "Morning Routine"
        assert len(routine.habits) == 0

    def test_add_habit_to_routine(self) -> None:
        time_provider = SystemTimeProvider()
        factory = StandardHabitFactory(time_provider)
        routine = factory.create_routine("Morning", "AM", "Health")
        exercise = factory.create_boolean_habit("Exercise", "Workout", "Health")
        routine.add_habit(exercise)
        assert len(routine.habits) == 1
        assert routine.habits[0] == exercise

    def test_remove_habit_from_routine(self) -> None:
        time_provider = SystemTimeProvider()
        factory = StandardHabitFactory(time_provider)
        routine = factory.create_routine("Morning", "AM", "Health")
        exercise = factory.create_boolean_habit("Exercise", "Workout", "Health")
        routine.add_habit(exercise)
        routine.remove_habit(exercise)
        assert len(routine.habits) == 0

    def test_nested_routines(self) -> None:
        time_provider = SystemTimeProvider()
        factory = StandardHabitFactory(time_provider)
        daily = factory.create_routine("Daily", "Full day", "Health")
        morning = factory.create_routine("Morning", "AM", "Health")
        evening = factory.create_routine("Evening", "PM", "Health")
        exercise = factory.create_boolean_habit("Exercise", "Workout", "Health")
        reading = factory.create_boolean_habit("Read", "Book", "Learning")
        morning.add_habit(exercise)
        evening.add_habit(reading)
        daily.add_habit(morning)
        daily.add_habit(evening)
        exercise.add_log(BooleanLog(date=date(2025, 1, 1), completed=True))
        reading.add_log(BooleanLog(date=date(2025, 1, 1), completed=True))
        progress = daily.get_progress()
        assert progress == 1.0


class TestHabitPolymorphism:
    def test_all_habits_have_get_progress(self) -> None:
        time_provider = SystemTimeProvider()
        factory = StandardHabitFactory(time_provider)
        habits: list[Habit] = [
            factory.create_boolean_habit("Exercise", "Daily", "Health"),
            factory.create_routine("Morning", "AM", "Health"),
        ]
        for habit in habits:
            progress = habit.get_progress()
            assert isinstance(progress, float)
            assert 0.0 <= progress <= 1.0

    def test_all_habits_have_get_statistics(self) -> None:
        time_provider = SystemTimeProvider()
        factory = StandardHabitFactory(time_provider)
        habits: list[Habit] = [
            factory.create_boolean_habit("Exercise", "Daily", "Health"),
            factory.create_numeric_habit("Water", "8 glasses", "Health", 8.0),
            factory.create_routine("Morning", "AM", "Health"),
        ]
        for habit in habits:
            stats = habit.get_statistics()
            assert isinstance(stats, Statistics)
