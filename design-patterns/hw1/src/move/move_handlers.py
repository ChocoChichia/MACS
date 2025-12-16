from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, cast

from src.constraints.config_movements import MOVEMENT_DATA
from src.constraints.enums import MovementType
from src.features.damage_feature import DamageComponent
from src.move.move_strategies import (
    CrawlStrategy,
    FlyStrategy,
    HopStrategy,
    MovementStrategy,
    NoStrategy,
    RunStrategy,
    WalkStrategy,
)

if TYPE_CHECKING:
    from src.creature import Creature


def _unwrap_creature(component: DamageComponent) -> Creature:
    from src.creature import Creature

    current = component
    while hasattr(current, "_wrapped"):
        current = current._wrapped
    return cast(Creature, current)


class MovementHandler(ABC):
    _next_handler: MovementHandler | None = None

    def set_next(self, handler: MovementHandler) -> MovementHandler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, component: DamageComponent) -> MovementStrategy:
        pass


class BaseMovementHandler(MovementHandler):
    def __init__(
        self, movement_type: MovementType, strategy_class: type[MovementStrategy]
    ):
        self._move_data = MOVEMENT_DATA[movement_type]
        self._strategy_class = strategy_class

    def handle(self, component: DamageComponent) -> MovementStrategy:
        base_creature = _unwrap_creature(component)

        if (
            self._move_data.requirement().is_satisfied_by(component)
            and base_creature.stamina >= self._move_data.stamina_required
            and base_creature.stamina >= self._move_data.stamina_usage
        ):
            return self._strategy_class()

        if self._next_handler:
            return self._next_handler.handle(component)

        return NoStrategy()


class FlyHandler(BaseMovementHandler):
    def __init__(self) -> None:
        super().__init__(MovementType.FLYING, FlyStrategy)


class RunHandler(BaseMovementHandler):
    def __init__(self) -> None:
        super().__init__(MovementType.RUNNING, RunStrategy)


class WalkHandler(BaseMovementHandler):
    def __init__(self) -> None:
        super().__init__(MovementType.WALKING, WalkStrategy)


class HopHandler(BaseMovementHandler):
    def __init__(self) -> None:
        super().__init__(MovementType.HOPPING, HopStrategy)


class CrawlHandler(BaseMovementHandler):
    def __init__(self) -> None:
        super().__init__(MovementType.CRAWLING, CrawlStrategy)
