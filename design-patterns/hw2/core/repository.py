from typing import Protocol

from core.habit import Habit
from core.logs import Log


class HabitRepository(Protocol):
    def save(self, habit: Habit) -> None:
        """
        Save a habit.

        Raises:
            RepositoryError: If the save operation fails.
        """
        ...

    def get_by_id(self, habit_id: str) -> Habit:
        """
        Retrieve a habit by ID.

        Args:
            habit_id: The unique identifier of the habit.

        Returns:
            The habit with the given ID.

        Raises:
            HabitNotFoundError: If no habit exists with the given ID.
            RepositoryError: If the retrieval operation fails.
        """
        ...

    def list_all(self) -> list[Habit]:
        """
        List all habits.

        Returns:
            A list of all habits.

        Raises:
            RepositoryError: If the listing operation fails.
        """
        ...

    def delete(self, habit_id: str) -> None:
        """
        Delete a habit by ID.

        Args:
            habit_id: The unique identifier of the habit to delete.

        Raises:
            HabitNotFoundError: If no habit exists with the given ID.
            RepositoryError: If the deletion operation fails.
        """
        ...


class LogRepository(Protocol):
    def add_log(self, habit_id: str, log: Log) -> None:
        """
        Add a log entry for a habit.

        Args:
            habit_id: The unique identifier of the habit.
            log: The log entry to add.

        Raises:
            HabitNotFoundError: If no habit exists with the given ID.
            RepositoryError: If the add operation fails.
        """
        ...

    def get_logs(self, habit_id: str) -> list[Log]:
        """
        Retrieve all logs for a habit.

        Args:
            habit_id: The unique identifier of the habit.

        Returns:
            A list of all log entries for the habit.

        Raises:
            HabitNotFoundError: If no habit exists with the given ID.
            RepositoryError: If the retrieval operation fails.
        """
        ...
