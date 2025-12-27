class Role:
    def __init__(self, key, name, faction, subfaction, tags, data, abilities):
        self.key = key
        self.name = name
        self.faction = faction
        self.subfaction = subfaction
        self.tags = set(tags)
        self.data = data
        self.abilities = list(abilities)

class RoleData:
    def __init__(self, investigator_result):
        self.investigator_result = investigator_result

class Player:
    def __init__(self, pid, name, role):
        self.id = pid
        self.name = name
        self.role = role
        self.alive = True
        self.defense = 0
        self.status = set()

class ActionIntent:
    def __init__(self, actor, ability_key, target, payload, priority):
        self.actor = actor
        self.ability_key = ability_key
        self.target = target
        self.payload = payload
        self.priority = priority

class GameEvent:
    def __init__(self, event_type, actor, target, message="", target_message=""):
        self.type = event_type
        self.actor = actor
        self.target = target
        self.message = message
        self.target_message = target_message

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
        self.protection_bonus[target_id] = max(bonus, self.protection_bonus.get(target_id, 0))

    def get_protection_bonus(self, target_id):
        return self.protection_bonus.get(target_id, 0)