class NightContext:
    def __init__(self):
        self.events = []
        self.visits = {}
        self.roleblocked = set()
        self.protection_bonus = {}

    def add_event(self, event):
        self.events.append(event)

    def add_visit(self, actor, target):
        self.visits.setdefault(target, []).append(actor)

    def is_roleblocked(self, pid):
        return pid in self.roleblocked

    def add_protection(self, target_id, bonus):
        self.protection_bonus[target_id] = max(
            bonus,
            self.protection_bonus.get(target_id, 0)
        )

    def get_protection_bonus(self, target_id):
        return self.protection_bonus.get(target_id, 0)