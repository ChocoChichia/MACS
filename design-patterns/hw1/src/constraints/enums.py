from enum import Enum, auto


class MovementType(Enum):
    CRAWLING = auto()
    HOPPING = auto()
    WALKING = auto()
    RUNNING = auto()
    FLYING = auto()
