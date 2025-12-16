from __future__ import annotations

import logging
from typing import cast

from src.constraints.constraints import Constraints
from src.creature import Creature
from src.features.damage_feature import DamageComponent
from src.simulation.interfaces import FightEngine

logger = logging.getLogger(__name__)


def _unwrap_creature(component: DamageComponent) -> Creature:
    current = component
    while hasattr(current, "_wrapped"):
        current = current._wrapped
    return cast(Creature, current)


class SimpleFightEngine(FightEngine):
    def fight(self, predator: DamageComponent, prey: DamageComponent) -> str:
        pred_base = _unwrap_creature(predator)
        prey_base = _unwrap_creature(prey)

        round_no = 0
        while pred_base.is_alive() and prey_base.is_alive():
            round_no += 1
            dmg = predator.get_power()
            prey_base.health -= dmg
            logger.info(
                f"Round {round_no}: Predator strikes Prey for"
                f"{dmg} damage (Prey health: {prey_base.health})"
            )
            if not prey_base.is_alive():
                logger.info(Constraints.PREDATOR_WON)
                return Constraints.PREDATOR_WON

            dmg = prey.get_power()
            pred_base.health -= dmg
            logger.info(
                f"Round {round_no}: Prey counters Predator for {dmg}"
                f"damage (Predator health: {pred_base.health})"
            )
            if not pred_base.is_alive():
                logger.info(Constraints.PREY_WON)
                return Constraints.PREY_WON

        if pred_base.is_alive():
            return Constraints.PREDATOR_WON
        return Constraints.PREY_WON
