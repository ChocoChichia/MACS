from dataclasses import dataclass

from src.constraints.enums import MovementType
from src.features.move_feature import (
    CanCrawlSpecification,
    CanFlySpecification,
    CanHopSpecification,
    CanRunSpecification,
    CanWalkSpecification,
    Specification,
)


@dataclass(frozen=True)
class MovementData:
    name: str
    stamina_usage: int
    stamina_required: int
    speed: int
    requirement: type[Specification]


MOVEMENT_DATA = {
    MovementType.CRAWLING: MovementData(
        name="Crawling",
        stamina_usage=1,
        stamina_required=0,
        speed=1,
        requirement=CanCrawlSpecification,
    ),
    MovementType.HOPPING: MovementData(
        name="Hopping",
        stamina_usage=2,
        stamina_required=20,
        speed=3,
        requirement=CanHopSpecification,
    ),
    MovementType.WALKING: MovementData(
        name="Walking",
        stamina_usage=2,
        stamina_required=40,
        speed=4,
        requirement=CanWalkSpecification,
    ),
    MovementType.RUNNING: MovementData(
        name="Running",
        stamina_usage=4,
        stamina_required=60,
        speed=6,
        requirement=CanRunSpecification,
    ),
    MovementType.FLYING: MovementData(
        name="Flying",
        stamina_usage=4,
        stamina_required=80,
        speed=8,
        requirement=CanFlySpecification,
    ),
}
