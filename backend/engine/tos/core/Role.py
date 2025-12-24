from abc import ABC, abstractmethod
from backend.engine.tos.enums.enums import Defense, Attack, Alignment, SubAlignment, Suspicious

class Role(ABC):
    @abstractmethod
    def getName(self) -> str: ...

    @abstractmethod
    def getDescription(self) -> str: ...

    @abstractmethod
    def getAlignment(self) -> Alignment: ...

    @abstractmethod
    def getSubAlignment(self) -> SubAlignment: ...

    @abstractmethod
    def isSuspicious(self) -> Suspicious: ...

    def getDefense(self) -> Defense:
        return Defense.NONE

    def getAttack(self) -> Attack:
        return Attack.NONE

    @abstractmethod
    def action(self, target): ...