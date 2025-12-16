from __future__ import annotations

import logging
import random
from typing import cast

from src.constraints.constraints import Constraints
from src.creature import Creature, CreatureBuilder
from src.evolution.evolution_step import WeaponEvolutionFactory
from src.evolution.limb_evolution import LegEvolution, WingEvolution
from src.evolution.weapon_evolution import (
    PredatorEvolutionFactory,
    PreyEvolutionFactory,
)
from src.features.damage_feature import DamageComponent

from .interfaces import EvolutionEngine

logger = logging.getLogger(__name__)


class DefaultEvolutionEngine(EvolutionEngine):
    def _evolve_creature(
        self,
        name: str,
        location: int,
        weapon_factory: WeaponEvolutionFactory,
        leg_weights: list[float],
        wing_weights: list[float],
    ) -> DamageComponent:
        claw_size = weapon_factory.create_claw_evolution().evolve()
        teeth_sharpness = weapon_factory.create_teeth_evolution().evolve()
        num_legs = LegEvolution(leg_weights).evolve()
        num_wings = WingEvolution(wing_weights).evolve()

        creature = (
            CreatureBuilder()
            .with_name(name)
            .with_location(location)
            .with_claws(claw_size)
            .with_teeth(teeth_sharpness)
            .with_legs(num_legs)
            .with_wings(num_wings)
            .build()
        )

        base_creature = self._get_base_creature(creature)
        logger.info(
            f"""
        🧬 Evolved Creature: {name}
        📍 Location: {location}

        ✨ Stats:
            🦵 Legs .............. {base_creature.legs}
            🪽 Wings ............. {base_creature.wings}
            🐾 Claws ............. {base_creature.claw_size!r}
            🦷 Teeth ............. {base_creature.teeth_sharpness!r}

        💥 Final Power: {creature.get_power()}
        """.strip()
        )
        return creature

    def _get_base_creature(self, component: DamageComponent) -> Creature:
        current = component
        while hasattr(current, "_wrapped"):
            current = current._wrapped
        return cast(Creature, current)

    def evolve_predator(self) -> DamageComponent:
        logger.info("--- EVOLUTION PHASE: PREDATOR ---")
        return self._evolve_creature(
            name="Predator",
            location=Constraints.DEFAULT_LOCATION,
            weapon_factory=PredatorEvolutionFactory(),
            leg_weights=Constraints.PREDATOR_LEG_WEIGHTS,
            wing_weights=Constraints.PREDATOR_WINGS_WEIGHTS,
        )

    def evolve_prey(self) -> DamageComponent:
        logger.info("--- EVOLUTION PHASE: PREY ---")
        return self._evolve_creature(
            name="Prey",
            location=random.randint(1, 1000),
            weapon_factory=PreyEvolutionFactory(),
            leg_weights=Constraints.PREY_LEG_WEIGHTS,
            wing_weights=Constraints.PREY_WINGS_WEIGHTS,
        )
