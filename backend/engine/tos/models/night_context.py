class NightContext:
    def __init__(self):
        self.events = []
        self.visits = {}
        self.protection_bonus = {}

    def add_event(self, event):
        self.events.append(event)

    def add_visit(self, actor, target):
        self.visits.setdefault(target, []).append(actor)

    def visit_count(self, target):
        return len(self.visits.get(target, []))

    def get_visits(self, target):
        return list(self.visits.get(target, []))

    def add_protection(self, target_id, bonus):
        self.protection_bonus[target_id] = max(
            bonus,
            self.protection_bonus.get(target_id, 0)
        )

    def get_protection_bonus(self, target_id):
        return self.protection_bonus.get(target_id, 0)
