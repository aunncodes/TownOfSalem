from backend.engine.tos.models.role import Role


class Player:
    def __init__(self, pid, name, role: Role):
        self.id = pid
        self.name = name
        self.role = role
        self.alive = True
        self.defense = 0
        self.status = set()