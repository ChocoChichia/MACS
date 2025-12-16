import random
from typing import Any

from src.constraints.constraints import Constraints
from src.evolution.evolution_step import (
    EvolutionStep,
    WeaponEvolutionFactory,
)


class WeightedWeaponEvolution(EvolutionStep):
    def __init__(self, parts_dict: dict[str, Any], weights: list[float]):
        self._parts = list(parts_dict.keys())
        self._weights = weights

    def evolve(self) -> str:
        return random.choices(self._parts, weights=self._weights, k=1)[0]


class OptionalEvolutionDecorator(EvolutionStep):
    def __init__(self, wrapped_evolution: EvolutionStep, chance_to_evolve: float):
        self._wrapped_evolution = wrapped_evolution
        self._chance_to_evolve = chance_to_evolve

    def evolve(self) -> str | None:
        if random.random() < self._chance_to_evolve:
            result = self._wrapped_evolution.evolve()
            return str(result) if result is not None else None
        return None


class BaseWeaponFactory(WeaponEvolutionFactory):
    def __init__(
        self,
        claw_weights: list[float],
        teeth_weights: list[float],
        is_optional: bool = False,
        chance_to_evolve: float = 1.0,
    ):
        self._claw_weights = claw_weights
        self._teeth_weights = teeth_weights
        self._is_optional = is_optional
        self._chance_to_evolve = chance_to_evolve

    def create_claw_evolution(self) -> EvolutionStep:
        evolution = WeightedWeaponEvolution(
            parts_dict=Constraints.CLAWS_MULTIPLIERS, weights=self._claw_weights
        )
        if self._is_optional:
            return OptionalEvolutionDecorator(evolution, self._chance_to_evolve)
        return evolution

    def create_teeth_evolution(self) -> EvolutionStep:
        evolution = WeightedWeaponEvolution(
            parts_dict=Constraints.TEETH_ADDITIVES, weights=self._teeth_weights
        )
        if self._is_optional:
            return OptionalEvolutionDecorator(evolution, self._chance_to_evolve)
        return evolution


class PredatorEvolutionFactory(BaseWeaponFactory):
    def __init__(self) -> None:
        super().__init__(
            claw_weights=Constraints.PREDATOR_CLAWS_WEIGHTS,
            teeth_weights=Constraints.PREDATOR_TEETH_WEIGHTS,
            is_optional=False,
        )


class PreyEvolutionFactory(BaseWeaponFactory):
    def __init__(self) -> None:
        super().__init__(
            claw_weights=Constraints.PREY_CLAWS_WEIGHTS,
            teeth_weights=Constraints.PREY_TEETH_WEIGHTS,
            is_optional=True,
            chance_to_evolve=Constraints.PREY_CHANCE_TO_EVOLVE_WEAPON,
        )
