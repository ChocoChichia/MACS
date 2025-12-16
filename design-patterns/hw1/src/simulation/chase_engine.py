from __future__ import annotations

import logging
from typing import cast

from src.constraints.constraints import Constraints
from src.creature import Creature
from src.features.damage_feature import DamageComponent
from src.simulation.interfaces import ChaseEngine

from .movement_selector import build_default_movement_chain, choose_strategy

logger = logging.getLogger(__name__)


def _unwrap_creature(component: DamageComponent) -> Creature:
    current = component
    while hasattr(current, "_wrapped"):
        current = current._wrapped
    return cast(Creature, current)


class GreedyChaseEngine(ChaseEngine):
    def __init__(self, max_steps: int = 10_000):
        self._handler = build_default_movement_chain()
        self._max_steps = max_steps

    def chase(self, predator: DamageComponent, prey: DamageComponent) -> bool:
        step = 0
        pred_base = _unwrap_creature(predator)
        prey_base = _unwrap_creature(prey)

        while step < self._max_steps:
            step += 1
            predator_strategy = choose_strategy(self._handler, predator)
            prey_strategy = choose_strategy(self._handler, prey)

            predator_strategy.move(predator)
            prey_strategy.move(prey)

            logger.debug(
                f"Step {step}: Predator at {pred_base.location}"
                f"(stamina={pred_base.stamina}), "
                f"Prey at {prey_base.location} (stamina={prey_base.stamina})"
            )

            if pred_base.stamina <= 0:
                logger.info(
                    f"Predator exhausted at location {pred_base.location}"
                    f"after {step} steps"
                )
                logger.info(Constraints.PREY_WON)
                return False

            if pred_base.location >= prey_base.location:
                logger.info(
                    f"Predator caught Prey at location"
                    f"{pred_base.location} on step {step}"
                )
                return True

        logger.warning(
            f"Chase reached maximum {self._max_steps}steps without conclusion"
        )
        return False
