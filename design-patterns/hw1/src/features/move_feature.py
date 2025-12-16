from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from src.creature import Creature
    from src.features.damage_feature import DamageComponent


def _unwrap_creature(component: DamageComponent) -> Creature:
    from src.creature import Creature

    current = component
    while hasattr(current, "_wrapped"):
        current = current._wrapped
    return cast(Creature, current)


class Specification(ABC):
    @abstractmethod
    def is_satisfied_by(self, component: DamageComponent) -> bool:
        pass


class CanFlySpecification(Specification):
    def is_satisfied_by(self, component: DamageComponent) -> bool:
        base_creature = _unwrap_creature(component)
        return base_creature.wings >= 2


class CanRunSpecification(Specification):
    def is_satisfied_by(self, component: DamageComponent) -> bool:
        base_creature = _unwrap_creature(component)
        return base_creature.legs >= 2


class CanWalkSpecification(Specification):
    def is_satisfied_by(self, component: DamageComponent) -> bool:
        base_creature = _unwrap_creature(component)
        return base_creature.legs >= 2


class CanHopSpecification(Specification):
    def is_satisfied_by(self, component: DamageComponent) -> bool:
        base_creature = _unwrap_creature(component)
        return base_creature.legs >= 1


class CanCrawlSpecification(Specification):
    def is_satisfied_by(self, component: DamageComponent) -> bool:
        base_creature = _unwrap_creature(component)
        return base_creature.is_alive()
