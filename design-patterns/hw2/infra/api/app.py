from fastapi import FastAPI

from core.errors import (
    HabitNotFoundError,
    InvalidGoalError,
    InvalidLogValueError,
    RepositoryError,
)
from infra.api.exception_handlers import (
    habit_not_found_handler,
    invalid_domain_error_handler,
    repository_error_handler,
)
from infra.api.routers import habits, logs


def create_app() -> FastAPI:
    app = FastAPI(
        title="Smart Habit Tracker API",
        version="0.1.0",
    )

    app.add_exception_handler(HabitNotFoundError, habit_not_found_handler)
    app.add_exception_handler(InvalidGoalError, invalid_domain_error_handler)
    app.add_exception_handler(InvalidLogValueError, invalid_domain_error_handler)
    app.add_exception_handler(RepositoryError, repository_error_handler)

    app.include_router(habits.router, prefix="/habits", tags=["Habits"])
    app.include_router(logs.router, prefix="/habits", tags=["Logs"])
    return app


app = create_app()
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("infra.api.app:app", host="0.0.0.0", port=8000, reload=True)
