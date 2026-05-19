from enum import Enum, auto

class GameEventType(Enum):
    SHERIFF_RESULT = auto()
    KILL = auto()
    ATTACK_BLOCKED = auto()
    TARGET_ROLEBLOCKED = auto()
    INVESTIGATION_RESULT = auto()
    JAIL_SELECTED = auto()