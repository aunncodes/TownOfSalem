from enum import Enum

class Alignment(str, Enum):
    TOWN = "TOWN"
    NEUTRAL = "NEUTRAL"
    MAFIA = "MAFIA"

class SubAlignment(str, Enum):
    KILLING = "KILLING"
    INVESTIGATIVE = "INVESTIGATIVE"
    PROTECTIVE = "PROTECTIVE"

class Suspicious(str, Enum):
    SUSPICIOUS = "SUSPICIOUS"
    INNOCENT = "INNOCENT"

class Defense(int, Enum):
    NONE = 0
    BASIC = 1
    POWERFUL = 2
    INVINCIBLE = 3

class Attack(int, Enum):
    NONE = 0
    BASIC = 1
    POWERFUL = 2
    INSTANT = 3