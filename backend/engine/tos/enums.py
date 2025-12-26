from enum import Enum, auto


class Faction(Enum):
    TOWN = auto()
    MAFIA = auto()
    NEUTRAL = auto()


class Phase(Enum):
    DAY = auto()
    NIGHT = auto()


class Tag(Enum):
    KILLING = auto()
    INVESTIGATIVE = auto()
    PROTECTIVE = auto()
    ROLEBLOCK_IMMUNE = auto()