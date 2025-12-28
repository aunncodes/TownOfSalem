class ActionIntent:
    def __init__(self, actor, ability_key, target, payload, priority):
        self.actor = actor
        self.ability_key = ability_key
        self.target = target
        self.payload = payload
        self.priority = priority