from backend.engine.tos.abilities.base import NightAbility
from backend.engine.tos.enums.game_event import GameEventType
from backend.engine.tos.enums.status import Status
from backend.engine.tos.models.events import GameEvent


class VeteranAbility(NightAbility):
    key = "alert"
    priority = 1

    def __init__(self):
        self.alerts_left = 3

    def apply(self, state, intent, ctx):
        if self.alerts_left <= 0:
            return
        self.alerts_left -= 1

        actor = state.require_player(intent.actor)
        actor.status.add(Status.ALERT)
        ctx.add_protection(intent.actor, 1)
        ctx.add_event(GameEvent(
            event_type=GameEventType.VETERAN_ALERTED,
            actor=intent.actor,
            messages={}
        ))