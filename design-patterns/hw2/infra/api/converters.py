from collections.abc import Callable
from datetime import date
from functools import singledispatch

from core.errors import InvalidLogValueError
from core.habit import Habit, HabitFactory, HabitType, Routine, SimpleHabit
from core.logs import BooleanLog, Log, NumericLog
from core.stats import NumericGoal, Statistics
from infra.api.schemas.habit import (
    BooleanHabitRead,
    CreateBooleanHabit,
    CreateNumericHabit,
    CreateRoutine,
    HabitBase,
    HabitRead,
    NumericHabitRead,
    RoutineRead,
)
from infra.api.schemas.log import BooleanLogRead, LogCreate, LogRead, NumericLogRead
from infra.api.schemas.stat import StatisticsRead


# ------------------- for habits -------------------------------
@singledispatch
def to_domain(request: HabitBase, factory: HabitFactory) -> Habit:
    raise NotImplementedError(f"No handler registered for {type(request)}")


@to_domain.register
def _(request: CreateBooleanHabit, factory: HabitFactory) -> Habit:
    return factory.create_boolean_habit(
        name=request.name,
        description=request.description,
        category=request.category,
    )


@to_domain.register
def _(request: CreateNumericHabit, factory: HabitFactory) -> Habit:
    return factory.create_numeric_habit(
        name=request.name,
        description=request.description,
        category=request.category,
        goal_value=request.goal,
    )


@to_domain.register
def _(request: CreateRoutine, factory: HabitFactory) -> Habit:
    return factory.create_routine(
        name=request.name,
        description=request.description,
        category=request.category,
    )


@singledispatch
def to_response(habit: Habit) -> HabitRead:
    raise NotImplementedError(f"No handler registered for {type(habit)}")


@to_response.register
def _(habit: SimpleHabit) -> HabitRead:
    if habit.type == HabitType.BOOLEAN:
        return BooleanHabitRead(
            id=habit.id,
            name=habit.name,
            description=habit.description,
            category=habit.category,
        )
    if habit.type == HabitType.NUMERIC:
        if not isinstance(habit.goal, NumericGoal):
            raise ValueError(
                f"Expected NumericGoal for numeric habit, got {type(habit.goal)}"
            )
        return NumericHabitRead(
            id=habit.id,
            name=habit.name,
            description=habit.description,
            category=habit.category,
            goal=habit.goal.target,
        )
    raise ValueError(f"Unknown habit type: {habit.type}")


@to_response.register
def _(habit: Routine) -> HabitRead:
    return RoutineRead(
        id=habit.id,
        name=habit.name,
        description=habit.description,
        category=habit.category,
        subhabit_count=len(habit.habits),
    )


# ------------ for logss -----------------------------


@singledispatch
def log_to_response(log: Log) -> LogRead:
    raise NotImplementedError(f"No handler registered for {type(log)}")


@log_to_response.register
def _(log: BooleanLog) -> LogRead:
    return BooleanLogRead(
        date=log.date,
        completed=log.completed,
    )


@log_to_response.register
def _(log: NumericLog) -> LogRead:
    return NumericLogRead(
        date=log.date,
        value=log.value,
    )


def create_boolean_log(request: LogCreate) -> BooleanLog:
    return BooleanLog(date=request.date, completed=request.value > 0)


def create_numeric_log(request: LogCreate) -> NumericLog:
    return NumericLog(date=request.date, value=request.value)


_LOG_FACTORIES: dict[HabitType, Callable[[LogCreate], Log]] = {
    HabitType.BOOLEAN: create_boolean_log,
    HabitType.NUMERIC: create_numeric_log,
}


def log_to_domain(request: LogCreate, habit_type: HabitType) -> Log:
    if request.date > date.today():
        raise InvalidLogValueError(f"Cannot create log for future date: {request.date}")
    factory = _LOG_FACTORIES[habit_type]
    return factory(request)


# ---------------- for stats ----------------


def stat_to_response(stat: Statistics) -> StatisticsRead:
    return StatisticsRead(**stat.__dict__)
