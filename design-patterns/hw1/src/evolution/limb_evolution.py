import random

from src.evolution.evolution_step import EvolutionStep


class WeightedLimbEvolution(EvolutionStep):
    def __init__(self, choices: list[int], weights: list[float]):
        self._choices = choices
        self._weights = weights

    def evolve(self) -> int:
        return random.choices(self._choices, weights=self._weights, k=1)[0]


class LegEvolution(WeightedLimbEvolution):
    def __init__(self, weights: list[float]):
        super().__init__(choices=[0, 1, 2], weights=weights)


class WingEvolution(WeightedLimbEvolution):
    def __init__(self, weights: list[float]):
        super().__init__(choices=[0, 1, 2], weights=weights)
