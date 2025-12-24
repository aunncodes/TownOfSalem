from backend.engine.tos.core.Role import Role


class Player:
    def __init__(self, role, name):
        self.alive = True
        self.role = role
        self.name = name

    def getRole(self) -> Role:
        return self.role

    def isAlive(self):
        return self.alive

    def action(self, target):
        return self.getRole().action(target)

    def kill(self, attack):
        if attack > self.getRole().getDefense():
            self.alive = False
            return True
        return False
