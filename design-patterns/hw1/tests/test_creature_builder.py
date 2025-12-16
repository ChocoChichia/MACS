from typing import cast

from src.creature import Creature, CreatureBuilder
from src.features.damage_feature import ClawDecorator, DamageComponent, TeethDecorator


def _unwrap_creature(component: DamageComponent) -> Creature:
    """Helper function to get the base Creature from a decorated component."""
    current = component
    while hasattr(current, "_wrapped"):
        current = current._wrapped
    return cast(Creature, current)


def test_build_default_creature() -> None:
    builder = CreatureBuilder()
    creature_component = builder.build()
    creature = _unwrap_creature(creature_component)

    assert creature.name == "Creature"
    assert creature.location == 0
    assert creature.legs == 0
    assert creature.wings == 0
    assert creature.claw_size is None
    assert creature.teeth_sharpness is None
    assert creature_component.get_power() == 1


def test_build_creature_with_attributes() -> None:
    builder = CreatureBuilder()
    creature_component = (
        builder.with_name("Test Monster")
        .with_location(100)
        .with_legs(2)
        .with_wings(2)
        .build()
    )
    creature = _unwrap_creature(creature_component)

    assert creature.name == "Test Monster"
    assert creature.location == 100
    assert creature.legs == 2
    assert creature.wings == 2


def test_build_applies_claw_decorator() -> None:
    builder = CreatureBuilder()
    creature_component = builder.with_claws("BIG").build()
    assert isinstance(creature_component, ClawDecorator)
    assert creature_component.get_power() == 4


def test_build_applies_teeth_decorator() -> None:
    builder = CreatureBuilder()
    creature_component = builder.with_teeth("VICIOUS").build()
    assert isinstance(creature_component, TeethDecorator)
    assert creature_component.get_power() == 10


def test_build_applies_both_decorators() -> None:
    builder = CreatureBuilder()
    creature_component = builder.with_claws("BIG").with_teeth("VICIOUS").build()

    assert isinstance(creature_component, TeethDecorator)
    wrapped_component = creature_component._wrapped
    assert isinstance(wrapped_component, ClawDecorator)
    assert creature_component.get_power() == 13
