class DayContext:
    def __init__(self):
        self.events = []
        self.votes = {}
        self.selected_jail_targets: dict[int, int] = {} # Dict is Actor: Target