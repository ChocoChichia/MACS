from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from infra.api.app import app
from infra.api.dependencies import get_habit_repository, get_log_repository
from infra.persistance.in_memory import InMemoryHabitRepository, InMemoryLogRepository


@pytest.fixture
def repository() -> InMemoryHabitRepository:
    return InMemoryHabitRepository()


@pytest.fixture
def api(repository: InMemoryHabitRepository) -> Generator[TestClient]:
    app.dependency_overrides[get_habit_repository] = lambda: repository
    app.dependency_overrides[get_log_repository] = lambda: InMemoryLogRepository(
        repository
    )
    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
