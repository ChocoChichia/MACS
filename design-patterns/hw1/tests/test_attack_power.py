from src.creature import Creature
from src.features.damage_feature import ClawDecorator, TeethDecorator


def test_base_power() -> None:
    creature = Creature(base_power=1)
    assert creature.get_power() == 1


def test_power_with_small_claws() -> None:
    creature = Creature(base_power=1)
    decorated = ClawDecorator(creature, "SMALL")
    assert decorated.get_power() == 2


def test_power_with_big_claws() -> None:
    creature = Creature(base_power=1)
    decorated = ClawDecorator(creature, "BIG")
    assert decorated.get_power() == 4


def test_power_with_dull_teeth() -> None:
    creature = Creature(base_power=1)
    decorated = TeethDecorator(creature, "DULL")
    assert decorated.get_power() == 4


def test_power_with_vicious_teeth() -> None:
    creature = Creature(base_power=1)
    decorated = TeethDecorator(creature, "VICIOUS")
    assert decorated.get_power() == 10


def test_power_with_claws_and_teeth() -> None:
    creature = Creature(base_power=1)
    with_claws = ClawDecorator(creature, "MEDIUM")
    with_both = TeethDecorator(with_claws, "SHARP")
    assert with_both.get_power() == 9


def test_power_with_teeth_and_claws_reversed_order() -> None:
    creature = Creature(base_power=1)
    with_teeth = TeethDecorator(creature, "SHARP")
    with_both = ClawDecorator(with_teeth, "MEDIUM")
    assert with_both.get_power() == 21
