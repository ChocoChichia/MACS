from __future__ import annotations

from typing import TYPE_CHECKING

from src.move.move_handlers import (
    CrawlHandler,
    FlyHandler,
    HopHandler,
    MovementHandler,
    RunHandler,
    WalkHandler,
)
from src.move.move_strategies import MovementStrategy, NoStrategy

if TYPE_CHECKING:
    from src.features.damage_feature import DamageComponent


def build_default_movement_chain() -> MovementHandler:
    head = FlyHandler()
    head.set_next(RunHandler()).set_next(WalkHandler()).set_next(HopHandler()).set_next(
        CrawlHandler()
    )
    return head


def choose_strategy(
    handler_chain: MovementHandler, creature: DamageComponent
) -> MovementStrategy:
    strategy = handler_chain.handle(creature)
    if strategy is None:
        return NoStrategy()
    return strategy
