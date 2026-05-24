class ActionIntent:
    def __init__(self, actor, ability_key, target, priority):
        self.actor = actor
        self.ability_key = ability_key
        self.target = target
        self.priority = priority