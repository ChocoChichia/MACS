from typing import Any
from unittest.mock import ANY

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def reading_habit() -> dict[str, Any]:
    return {
        "name": "Reading",
        "description": "Read 10 pages",
        "category": "Education",
        "type": "boolean",
    }


@pytest.fixture
def running_habit() -> dict[str, Any]:
    return {
        "name": "Running",
        "description": "Run 5km",
        "category": "Health",
        "type": "numeric",
        "goal": 5.0,
    }


@pytest.fixture
def healthy_routine() -> dict[str, Any]:
    return {
        "name": "Basic Health",
        "description": "idk",
        "category": "Heidkalth",
        "type": "routine",
    }


def test_should_create(api: TestClient, reading_habit: dict[str, Any]) -> None:
    response = api.post("/habits", json=reading_habit)

    assert response.status_code == 201
    assert response.json() == {"id": ANY, **reading_habit}


def test_should_persist(api: TestClient, reading_habit: dict[str, Any]) -> None:
    response = api.post("/habits", json=reading_habit)
    habit_id = response.json()["id"]
    assert habit_id

    response = api.get(f"/habits/{habit_id}")

    assert response.status_code == 200
    assert response.json() == {"id": habit_id, **reading_habit}


def test_should_read_all(
    api: TestClient,
    reading_habit: dict[str, Any],
    running_habit: dict[str, Any],
) -> None:
    api.post("/habits", json=reading_habit)
    api.post("/habits", json=running_habit)

    response = api.get("/habits")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert {"id": ANY, **reading_habit} in data
    assert {"id": ANY, **running_habit} in data


def test_should_update(api: TestClient, reading_habit: dict[str, Any]) -> None:
    response = api.post("/habits", json=reading_habit)
    habit_id = response.json()["id"]

    updated_payload = reading_habit.copy()
    updated_payload["name"] = "Reading Advanced"
    updated_payload["description"] = "Read 50 pages"

    response = api.put(f"/habits/{habit_id}", json=updated_payload)

    assert response.status_code == 200
    assert response.json() == {"id": habit_id, **updated_payload}

    response = api.get(f"/habits/{habit_id}")
    assert response.json()["name"] == "Reading Advanced"


def test_should_delete(api: TestClient, reading_habit: dict[str, Any]) -> None:
    response = api.post("/habits", json=reading_habit)
    habit_id = response.json()["id"]

    response = api.delete(f"/habits/{habit_id}")
    assert response.status_code == 204

    response = api.get(f"/habits/{habit_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Habit with ID <{habit_id}> not found."}


def test_should_not_delete_unknown(api: TestClient) -> None:
    unknown_id = "non-existent-id"
    response = api.delete(f"/habits/{unknown_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Habit with ID <{unknown_id}> not found."}


def test_should_create_numeric(api: TestClient, running_habit: dict[str, Any]) -> None:
    response = api.post("/habits", json=running_habit)

    assert response.status_code == 201
    assert response.json() == {"id": ANY, **running_habit}


def test_add_subhabit(
    api: TestClient, reading_habit: dict[str, Any], healthy_routine: dict[str, Any]
) -> None:
    routine_res = api.post("/habits", json=healthy_routine)
    assert routine_res.status_code == 201
    routine_id = routine_res.json()["id"]

    habit_res = api.post("/habits", json=reading_habit)
    assert habit_res.status_code == 201
    subhabit_id = habit_res.json()["id"]

    response = api.post(
        f"/habits/{routine_id}/subhabits", json={"subhabit_id": subhabit_id}
    )

    assert response.status_code == 201

    expected_response = {"id": routine_id, **healthy_routine, "subhabit_count": 1}

    assert response.json() == expected_response
