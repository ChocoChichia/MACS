class HabitTrackerError(Exception):
    pass


class HabitNotFoundError(HabitTrackerError):
    def __init__(self, habit_id: str) -> None:
        super().__init__(f"Habit with ID <{habit_id}> not found.")
        self.habit_id = habit_id


class InvalidGoalError(HabitTrackerError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class InvalidLogValueError(HabitTrackerError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class RepositoryError(HabitTrackerError):
    def __init__(self, message: str) -> None:
        super().__init__(message)
