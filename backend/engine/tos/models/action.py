from backend.engine.tos.enums.phase import Phase

class ActionChoice:
    def __init__(self, name, actor, phase: Phase, requires_target: bool, description=None):
        self.name = name
        self.actor = actor
        self.phase = phase
        self.requires_target = requires_target
        self.description = description