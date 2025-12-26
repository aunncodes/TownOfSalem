class Role:
    def __init__(self, key, name, faction, tags=None, abilities=None):
        self.key = key
        self.name = name
        self.faction = faction
        self.tags = set(tags or [])
        self.abilities = list(abilities or [])


class Player:
    def __init__(self, pid, name, role):
        self.id = pid
        self.name = name
        self.role = role
        self.alive = True
        self.defense = 0
        self.status = set()


class ActionIntent:
    def __init__(self, actor, ability_key, target, payload=None):
        self.actor = actor
        self.ability_key = ability_key
        self.target = target
        self.payload = dict(payload or {})


class GameEvent:
    def __init__(self, event_type, actor, target, message="", public=False, data=None):
        self.type = event_type
        self.actor = actor
        self.target = target
        self.message = message
        self.public = public
        self.data = dict(data or {})


class GameState:
    def __init__(self, phase, players):
        self.phase = phase
        self.players = dict(players)

        self.queued = []

        self.visits_by_target = {}
        self.protection_bonus = {}
        self.roleblocked = set()

    def require_player(self, pid):
        if pid not in self.players:
            raise ValueError("Unknown player id: " + str(pid))
        return self.players[pid]

    def is_alive(self, pid):
        return self.require_player(pid).alive

    def queue_intent(self, intent):
        self.queued.append(intent)

    def clear_night_state(self):
        self.queued.clear()
        self.visits_by_target.clear()
        self.protection_bonus.clear()
        self.roleblocked.clear()
