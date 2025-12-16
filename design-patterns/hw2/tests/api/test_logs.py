from datetime import date, timedelta
from typing import Any

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
        "description": "Routine description",
        "category": "Health",
        "type": "routine",
    }


def test_should_add_log_boolean(api: TestClient, reading_habit: dict[str, Any]) -> None:
    h_res = api.post("/habits", json=reading_habit)
    habit_id = h_res.json()["id"]

    today = date.today().isoformat()
    log_payload = {"date": today, "value": 1.0}

    response = api.post(f"/habits/{habit_id}/logs", json=log_payload)

    assert response.status_code == 201
    assert response.json()["id"] == habit_id


def test_should_add_log_numeric(api: TestClient, running_habit: dict[str, Any]) -> None:
    h_res = api.post("/habits", json=running_habit)
    habit_id = h_res.json()["id"]

    today = date.today().isoformat()
    log_payload = {"date": today, "value": 3.5}

    response = api.post(f"/habits/{habit_id}/logs", json=log_payload)

    assert response.status_code == 201
    assert response.json()["id"] == habit_id


def test_should_list_boolean_logs(
    api: TestClient, reading_habit: dict[str, Any]
) -> None:
    h_res = api.post("/habits", json=reading_habit)
    habit_id = h_res.json()["id"]

    today = date.today().isoformat()
    api.post(f"/habits/{habit_id}/logs", json={"date": today, "value": 1.0})

    response = api.get(f"/habits/{habit_id}/logs")

    assert response.status_code == 200
    logs = response.json()
    assert len(logs) == 1

    assert logs[0] == {"date": today, "type": "boolean", "completed": True}


def test_should_list_numeric_logs(
    api: TestClient, running_habit: dict[str, Any]
) -> None:
    h_res = api.post("/habits", json=running_habit)
    habit_id = h_res.json()["id"]

    today = date.today().isoformat()
    api.post(f"/habits/{habit_id}/logs", json={"date": today, "value": 4.2})

    response = api.get(f"/habits/{habit_id}/logs")

    assert response.status_code == 200
    logs = response.json()
    assert len(logs) == 1

    assert logs[0] == {"date": today, "type": "numeric", "value": 4.2}


def test_should_get_stats_boolean(
    api: TestClient, reading_habit: dict[str, Any]
) -> None:
    h_res = api.post("/habits", json=reading_habit)
    habit_id = h_res.json()["id"]

    today = date.today()
    yesterday = today - timedelta(days=1)

    api.post(
        f"/habits/{habit_id}/logs", json={"date": yesterday.isoformat(), "value": 1.0}
    )
    api.post(f"/habits/{habit_id}/logs", json={"date": today.isoformat(), "value": 1.0})

    response = api.get(f"/habits/{habit_id}/stats")

    assert response.status_code == 200
    stats = response.json()

    assert stats == {
        "total_completions": 2,
        "current_streak": 2,
        "average_progress": 1.0,
    }


def test_should_get_stats_numeric(
    api: TestClient, running_habit: dict[str, Any]
) -> None:
    h_res = api.post("/habits", json=running_habit)
    habit_id = h_res.json()["id"]

    today = date.today().isoformat()
    api.post(f"/habits/{habit_id}/logs", json={"date": today, "value": 2.5})

    response = api.get(f"/habits/{habit_id}/stats")

    assert response.status_code == 200
    stats = response.json()

    assert stats == {
        "total_completions": 0,
        "current_streak": 0,
        "average_progress": 0.5,
    }


def test_should_not_log_unknown_habit(api: TestClient) -> None:
    today = date.today().isoformat()
    response = api.post(
        "/habits/non-existent-id/logs", json={"date": today, "value": 1.0}
    )

    assert response.status_code == 404
