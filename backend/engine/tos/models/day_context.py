class DayContext:
    def __init__(self):
        self.events = []
        self.votes = {}

    def add_event(self, event):
        self.events.append(event)