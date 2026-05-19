class DayContext:
    def __init__(self):
        self.events = []
        self.votes = {}
        self.jailed: dict[int, int] = {}  # actor: target

    def add_event(self, event):
        self.events.append(event)

    def select_jail_target(self, actor_id: int, target_id: int):
        self.jailed[actor_id] = target_id

    def get_selected_jail_target(self, actor_id: int):
        return self.jailed.get(actor_id)

    def get_all_jail_targets(self):
        return dict(self.jailed)