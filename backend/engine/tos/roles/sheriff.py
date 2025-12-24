from backend.engine.tos.core.Player import Player
from backend.engine.tos.core.Role import Role
from backend.engine.tos.enums.enums import Alignment, SubAlignment, Suspicious, Defense, Attack


class Sheriff(Role):
    def getName(self):
        return "Sheriff"

    def getDescription(self):
        return "Investigates a person."

    def getAlignment(self):
        return Alignment.TOWN

    def getSubAlignment(self):
        return SubAlignment.INVESTIGATIVE

    def isSuspicious(self):
        return Suspicious.INNOCENT

    def getDefense(self):
        return Defense.NONE

    def getAttack(self):
        return Attack.NONE

    def action(self, target: Player):
        if target.getRole().isSuspicious() == Suspicious.SUSPICIOUS:
            return "Your target is suspicious or framed!"
        else:
            return "Your target is innocent or good at hiding secrets..."