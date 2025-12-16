from unittest.mock import patch

from src.constraints.constraints import Constraints
from src.evolution.limb_evolution import LegEvolution, WingEvolution
from src.evolution.weapon_evolution import (
    OptionalEvolutionDecorator,
    PredatorEvolutionFactory,
    PreyEvolutionFactory,
    WeightedWeaponEvolution,
)


def test_weighted_weapon_evolution() -> None:
    parts = Constraints.CLAWS_MULTIPLIERS
    weights = [1.0, 0.0, 0.0]
    evolution = WeightedWeaponEvolution(parts, weights)
    assert evolution.evolve() == "SMALL"


def test_optional_evolution_decorator() -> None:
    parts = Constraints.CLAWS_MULTIPLIERS
    weights = [1.0, 0.0, 0.0]
    evolution = WeightedWeaponEvolution(parts, weights)

    with patch("random.random", return_value=0.1):
        optional_evolution = OptionalEvolutionDecorator(evolution, chance_to_evolve=0.5)
        assert optional_evolution.evolve() == "SMALL"

    with patch("random.random", return_value=0.9):
        optional_evolution = OptionalEvolutionDecorator(evolution, chance_to_evolve=0.5)
        assert optional_evolution.evolve() is None


def test_predator_factory_creates_non_optional() -> None:
    factory = PredatorEvolutionFactory()
    claw_evolution = factory.create_claw_evolution()
    assert not isinstance(claw_evolution, OptionalEvolutionDecorator)


def test_prey_factory_creates_optional() -> None:
    factory = PreyEvolutionFactory()
    claw_evolution = factory.create_claw_evolution()
    assert isinstance(claw_evolution, OptionalEvolutionDecorator)


def test_limb_evolution_returns_valid_counts() -> None:
    leg_evolution = LegEvolution(weights=[0.1, 0.2, 0.7])
    wing_evolution = WingEvolution(weights=[0.6, 0.2, 0.2])
    assert leg_evolution.evolve() in [0, 1, 2]
    assert wing_evolution.evolve() in [0, 1, 2]
