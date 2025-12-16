from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Protocol


class TimeProvider(Protocol):
    def today(self) -> date:
        """Return the current date."""
        ...


class SystemTimeProvider:
    def today(self) -> date:
        return date.today()


@dataclass(frozen=True)
class Log(ABC):
    date: date

    @abstractmethod
    def get_value(self) -> float:
        pass


@dataclass(frozen=True)
class NumericLog(Log):
    value: float

    def get_value(self) -> float:
        return self.value


@dataclass(frozen=True)
class BooleanLog(Log):
    completed: bool

    def get_value(self) -> float:
        return 1.0 if self.completed else 0.0
