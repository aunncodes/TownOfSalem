from enum import Enum, auto

class Status(Enum):
    FRAMED = auto()
    JAILED = auto()
    ALERT = auto()
    ROLEBLOCKED = auto()