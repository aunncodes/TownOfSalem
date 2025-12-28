class GameState:
    def __init__(self, phase, players):
        self.phase = phase
        self.players = dict(players)

        self.queued = []

    def require_player(self, pid):
        if pid not in self.players:
            raise ValueError("Unknown player id: " + str(pid))
        return self.players[pid]

    def is_alive(self, pid):
        return self.require_player(pid).alive

    def queue_intent(self, intent):
        self.queued.append(intent)

class GameEvent:
    def __init__(self, event_type, actor, target, message="", target_message=""):
        self.type = event_type
        self.actor = actor
        self.target = target
        self.message = message
        self.target_message = target_message