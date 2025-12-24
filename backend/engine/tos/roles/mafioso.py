from backend.engine.tos.core.Player import Player
from backend.engine.tos.core.Role import Role
from backend.engine.tos.enums.enums import Alignment, SubAlignment, Suspicious, Defense, Attack


class Mafioso(Role):
    def getName(self):
        return "Mafioso"

    def getDescription(self):
        return "Kills target"

    def getAlignment(self):
        return Alignment.MAFIA

    def getSubAlignment(self):
        return SubAlignment.KILLING

    def isSuspicious(self):
        return Suspicious.SUSPICIOUS

    def getDefense(self):
        return Defense.NONE

    def getAttack(self):
        return Attack.BASIC

    def action(self, target: Player):
        if target.kill(self.getAttack()):
            return "Your target has been killed."
        else:
            return "Your target's defense was too strong!"