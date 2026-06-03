from enum import Enum, auto

class GameEventType(Enum):
    SHERIFF_RESULT = auto()
    KILL = auto()
    ATTACK_BLOCKED = auto()
    TARGET_ROLEBLOCKED = auto()
    INVESTIGATION_RESULT = auto()
    JAIL_SELECTED = auto()
    TARGET_JAILED = auto()
    TARGET_PROTECTED = auto()
    VETERAN_ALERTED = auto()
    VETERAN_SHOT = auto()
    LOOKOUT_WATCH = auto()
    LOOKOUT_SAW = auto()