from abc import ABC, abstractmethod
from typing import Any


class EvolutionStep(ABC):
    @abstractmethod
    def evolve(self) -> Any:
        pass


class WeaponEvolutionFactory(ABC):
    @abstractmethod
    def create_claw_evolution(self) -> EvolutionStep:
        pass

    @abstractmethod
    def create_teeth_evolution(self) -> EvolutionStep:
        pass
