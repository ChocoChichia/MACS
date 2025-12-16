from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import cast

from src.constraints.config_movements import MOVEMENT_DATA
from src.constraints.enums import MovementType
from src.creature import Creature
from src.features.damage_feature import DamageComponent

logger = logging.getLogger(__name__)


def _unwrap_creature(component: DamageComponent) -> Creature:
    current = component
    while hasattr(current, "_wrapped"):
        current = current._wrapped
    return cast(Creature, current)


class MovementStrategy(ABC):
    @abstractmethod
    def move(self, creature: DamageComponent) -> None:
        pass


class MovementResult:
    def __init__(self, speed: int, stamina_usage: int):
        self.speed = speed
        self.stamina_usage = stamina_usage

    def apply_to(self, creature: DamageComponent) -> None:
        base_creature = _unwrap_creature(creature)
        base_creature.location += self.speed
        base_creature.stamina -= self.stamina_usage


class BaseMovementStrategy(MovementStrategy):
    def __init__(self, movement_type: MovementType):
        self._move_data = MOVEMENT_DATA[movement_type]

    def move(self, creature: DamageComponent) -> None:
        base_creature = _unwrap_creature(creature)
        logger.info(
            f"{base_creature.name} at location"
            f"{base_creature.location} is {self._move_data.name} "
            f"with speed {self._move_data.speed} "
            f"(stamina: {base_creature.stamina} -> "
            f"{base_creature.stamina - self._move_data.stamina_usage})"
        )
        MovementResult(
            speed=self._move_data.speed,
            stamina_usage=self._move_data.stamina_usage,
        ).apply_to(creature=creature)


class FlyStrategy(BaseMovementStrategy):
    def __init__(self) -> None:
        super().__init__(movement_type=MovementType.FLYING)


class RunStrategy(BaseMovementStrategy):
    def __init__(self) -> None:
        super().__init__(movement_type=MovementType.RUNNING)


class WalkStrategy(BaseMovementStrategy):
    def __init__(self) -> None:
        super().__init__(movement_type=MovementType.WALKING)


class HopStrategy(BaseMovementStrategy):
    def __init__(self) -> None:
        super().__init__(movement_type=MovementType.HOPPING)


class CrawlStrategy(BaseMovementStrategy):
    def __init__(self) -> None:
        super().__init__(movement_type=MovementType.CRAWLING)


class NoStrategy(MovementStrategy):
    def move(self, creature: DamageComponent) -> None:
        base_creature = _unwrap_creature(creature)
        logger.info(f"{base_creature.name} is exhausted and cannot move")
