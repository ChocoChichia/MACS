from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from src.constraints.constraints import Constraints

if TYPE_CHECKING:
    pass


class DamageComponent(ABC):
    @abstractmethod
    def get_power(self) -> int:
        pass


class DamageDecorator(DamageComponent):
    def __init__(self, component: DamageComponent) -> None:
        self._wrapped = component

    def get_power(self) -> int:
        return self._wrapped.get_power()


class ClawDecorator(DamageDecorator):
    def __init__(self, component: DamageComponent, size: str) -> None:
        super().__init__(component)
        self._multiplier = Constraints.CLAWS_MULTIPLIERS.get(size.upper(), 1)

    def get_power(self) -> int:
        base_power = super().get_power()
        return base_power * self._multiplier


class TeethDecorator(DamageDecorator):
    def __init__(self, component: DamageComponent, sharpness: str) -> None:
        super().__init__(component)
        self._bonus = Constraints.TEETH_ADDITIVES.get(sharpness.upper(), 0)

    def get_power(self) -> int:
        base_power = super().get_power()
        return base_power + self._bonus
