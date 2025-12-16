from __future__ import annotations

from dataclasses import dataclass, field

from src.constraints.constraints import Constraints
from src.features.damage_feature import ClawDecorator, DamageComponent, TeethDecorator


@dataclass
class Creature(DamageComponent):
    name: str = field(default="Creature")
    health: int = field(default=Constraints.DEFAULT_HEALTH)
    stamina: int = field(default=Constraints.DEFAULT_STAMINA)
    location: int = field(default=Constraints.DEFAULT_LOCATION)
    base_power: int = field(default=Constraints.DEFAULT_POWER)

    legs: int = field(default=0)
    wings: int = field(default=0)
    claw_size: str | None = field(default=None)
    teeth_sharpness: str | None = field(default=None)

    def get_power(self) -> int:
        return self.base_power

    def is_alive(self) -> bool:
        return self.health > 0


class CreatureBuilder:
    def __init__(self) -> None:
        self._name: str = "Creature"
        self._location: int = Constraints.DEFAULT_LOCATION
        self._legs: int = 0
        self._wings: int = 0
        self._claw_size: str | None = None
        self._teeth_sharpness: str | None = None

    def with_name(self, name: str) -> CreatureBuilder:
        self._name = name
        return self

    def with_location(self, location: int) -> CreatureBuilder:
        self._location = location
        return self

    def with_legs(self, count: int) -> CreatureBuilder:
        self._legs = count
        return self

    def with_wings(self, count: int) -> CreatureBuilder:
        self._wings = count
        return self

    def with_claws(self, size: str | None) -> CreatureBuilder:
        self._claw_size = size
        return self

    def with_teeth(self, sharpness: str | None) -> CreatureBuilder:
        self._teeth_sharpness = sharpness
        return self

    def build(self) -> DamageComponent:
        creature_component = Creature(
            name=self._name,
            location=self._location,
            legs=self._legs,
            wings=self._wings,
            claw_size=self._claw_size,
            teeth_sharpness=self._teeth_sharpness,
        )

        decorated_creature: DamageComponent = creature_component
        if self._claw_size:
            decorated_creature = ClawDecorator(decorated_creature, self._claw_size)
        if self._teeth_sharpness:
            decorated_creature = TeethDecorator(
                decorated_creature, self._teeth_sharpness
            )
        return decorated_creature
