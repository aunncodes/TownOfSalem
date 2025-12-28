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

class Phase(Enum):
    DAY = auto()
    NIGHT = auto()

class Tag(Enum):
    ROLEBLOCK_IMMUNE = auto()
    DETECTION_IMMUNE = auto()

class GameEventType(Enum):
    SHERIFF_RESULT = auto()
    KILL = auto()
    ATTACK_BLOCKED = auto()
    TARGET_ROLEBLOCKED = auto()
    INVESTIGATION_RESULT = auto()

class Status(Enum):
    FRAMED = auto()