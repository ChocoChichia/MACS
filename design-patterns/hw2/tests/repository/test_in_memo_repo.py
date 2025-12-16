import pytest

from core.errors import HabitNotFoundError
from core.habit import HabitType, SimpleHabit
from core.logs import SystemTimeProvider
from core.stats import BooleanGoal, StandardDailyProgress, StatisticsCalculator
from infra.persistance.in_memory import InMemoryHabitRepository


def create_dummy_habit(habit_id: str = "1", name: str = "Test Habit") -> SimpleHabit:
    return SimpleHabit(
        id=habit_id,
        name=name,
        description="A test habit",
        category="Test",
        goal=BooleanGoal(),
        type=HabitType.BOOLEAN,
        calculator=StatisticsCalculator(StandardDailyProgress(), SystemTimeProvider()),
    )


def test_should_not_get_unknown_habit() -> None:
    repository = InMemoryHabitRepository()

    with pytest.raises(HabitNotFoundError):
        repository.get_by_id("non-existent-id")


def test_should_persist_habit() -> None:
    repository = InMemoryHabitRepository()

    habit = create_dummy_habit(habit_id="1", name="Drink Water")

    repository.save(habit)

    retrieved = repository.get_by_id("1")

    assert retrieved == habit
    assert retrieved is not habit


def test_should_not_delete_unknown_habit() -> None:
    repository = InMemoryHabitRepository()

    with pytest.raises(HabitNotFoundError):
        repository.delete("non-existent-id")


def test_should_delete_habit() -> None:
    repository = InMemoryHabitRepository()
    habit = create_dummy_habit(habit_id="1")

    repository.save(habit)
    repository.delete("1")

    with pytest.raises(HabitNotFoundError):
        repository.get_by_id("1")


def test_should_list_all_habits() -> None:
    repository = InMemoryHabitRepository()

    habit1 = create_dummy_habit(habit_id="1", name="Habit One")
    habit2 = create_dummy_habit(habit_id="2", name="Habit Two")

    repository.save(habit1)
    repository.save(habit2)

    all_habits = repository.list_all()

    assert len(all_habits) == 2
    assert habit1 in all_habits
    assert habit2 in all_habits


def test_save_updates_existing_habit() -> None:
    repository = InMemoryHabitRepository()
    habit = create_dummy_habit(habit_id="1", name="Old Name")

    repository.save(habit)

    habit.name = "New Name"
    repository.save(habit)

    retrieved = repository.get_by_id("1")
    assert retrieved.name == "New Name"
