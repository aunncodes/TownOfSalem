from backend.engine.tos.abilities.base import TargetedNightAbility
from backend.engine.tos.enums.game_event import GameEventType
from backend.engine.tos.models.events import GameEvent
from backend.engine.tos.models.night_context import NightContext


class DoctorAbility(TargetedNightAbility):
    key = "protect"
    priority = 3
    payload = {"defense_bonus": 1}

    def apply(self, state, intent, ctx: NightContext):
        bonus = int(intent.payload.get("defense_bonus", 1))
        ctx.add_protection(intent.target, bonus)
        ctx.add_event(GameEvent(
            event_type=GameEventType.TARGET_PROTECTED,
            actor=intent.actor,
            target=intent.target,
            messages={} # No guaranteed message, only for the sake of logs.
        ))