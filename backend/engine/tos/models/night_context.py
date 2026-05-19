from backend.engine.tos.enums.status import Status

class NightContext:
    def __init__(self):
        self.events = []
        self.visits = {}
        self.roleblocked = set()
        self.protection_bonus = {}

        self.jailed_by = {}      # target -> jailor
        self.jail_targets = {}   # jailor -> target

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

    def jail_player(self, state, jailor_id, target_id):
        target = state.require_player(target_id)

        self.jail_targets[jailor_id] = target_id
        self.jailed_by[target_id] = jailor_id
        target.status.add(Status.JAILED)

    def is_jailed(self, pid):
        return pid in self.jailed_by

    def get_jailor_for(self, target_id):
        return self.jailed_by.get(target_id)

    def get_jailed_target_for(self, jailor_id):
        return self.jail_targets.get(jailor_id)

    def clear_jails(self, state):
        for target_id in self.jailed_by:
            player = state.require_player(target_id)
            player.status.discard(Status.JAILED)

        self.jailed_by.clear()
        self.jail_targets.clear()