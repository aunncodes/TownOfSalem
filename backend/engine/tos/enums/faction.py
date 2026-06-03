from enum import Enum, auto

class Faction(Enum):
    TOWN = auto()
    MAFIA = auto()
    NEUTRAL = auto()

class SubFaction(Enum):
    KILLING = auto()
    INVESTIGATIVE = auto()
    PROTECTIVE = auto()
    SUPPORT = auto()
    DECEPTION = auto()