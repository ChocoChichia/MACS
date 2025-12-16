from __future__ import annotations

from abc import ABC, abstractmethod

from src.features.damage_feature import DamageComponent


class EvolutionEngine(ABC):
    @abstractmethod
    def evolve_predator(self) -> DamageComponent:
        pass

    @abstractmethod
    def evolve_prey(self) -> DamageComponent:
        pass


class ChaseEngine(ABC):
    @abstractmethod
    def chase(self, predator: DamageComponent, prey: DamageComponent) -> bool:
        pass


class FightEngine(ABC):
    @abstractmethod
    def fight(self, predator: DamageComponent, prey: DamageComponent) -> str:
        pass
