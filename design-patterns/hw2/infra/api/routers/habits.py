from fastapi import APIRouter, HTTPException, Response, status

from core.habit import Routine, SimpleHabit
from infra.api.converters import to_domain, to_response
from infra.api.dependencies import FactoryDep, HabitRepoDep
from infra.api.schemas.habit import AddSubHabitRequest, CreateHabitRequest, HabitRead

router = APIRouter()


@router.post(
    "",
    response_model=HabitRead,
    status_code=status.HTTP_201_CREATED,
)
def create_habit(
    request: CreateHabitRequest,
    factory: FactoryDep,
    repository: HabitRepoDep,
) -> HabitRead:
    habit = to_domain(request, factory)
    repository.save(habit)

    return to_response(habit)


@router.get(
    "",
    response_model=list[HabitRead],
)
def list_habits(
    repository: HabitRepoDep,
) -> list[HabitRead]:
    habits = repository.list_all()

    return [to_response(habit) for habit in habits]


@router.get(
    "/{habit_id}",
    response_model=HabitRead,
)
def read_habit(
    habit_id: str,
    repository: HabitRepoDep,
) -> HabitRead:
    habit = repository.get_by_id(habit_id)

    return to_response(habit)


@router.put(
    "/{habit_id}",
    response_model=HabitRead,
)
def update_habit(
    habit_id: str,
    request: CreateHabitRequest,
    factory: FactoryDep,
    repository: HabitRepoDep,
) -> HabitRead:
    existing_habit = repository.get_by_id(habit_id)
    updated_habit = to_domain(request, factory)
    updated_habit.id = habit_id

    if isinstance(existing_habit, SimpleHabit) and isinstance(
        updated_habit, SimpleHabit
    ):
        updated_habit.logs = existing_habit.get_logs()

    repository.save(updated_habit)

    return to_response(updated_habit)


@router.delete(
    "/{habit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_habit(
    habit_id: str,
    repository: HabitRepoDep,
) -> Response:
    repository.delete(habit_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{habit_id}/subhabits",
    response_model=HabitRead,
    status_code=status.HTTP_201_CREATED,
)
def add_subhabit(
    habit_id: str,
    request: AddSubHabitRequest,
    repository: HabitRepoDep,
) -> HabitRead:
    routine = repository.get_by_id(habit_id=habit_id)
    if not isinstance(routine, Routine):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Habit <{habit_id}> is not a routine.",
        )

    subhabit = repository.get_by_id(habit_id=request.subhabit_id)
    routine.add_habit(subhabit)
    repository.save(routine)

    return to_response(routine)
