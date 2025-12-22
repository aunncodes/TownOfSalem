from enum import Enum

class GamePhase(str, Enum):
    LOBBY = "LOBBY"
    DAY = "DAY"
    VOTING = "VOTING"
    NIGHT = "NIGHT"
