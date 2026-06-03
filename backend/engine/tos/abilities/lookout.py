from backend.engine.tos.abilities.base import TargetedNightAbility
from backend.engine.tos.enums.game_event import GameEventType
from backend.engine.tos.enums.status import StatusType
from backend.engine.tos.models.events import GameEvent
from backend.engine.tos.models.night_context import NightContext


class LookoutAbility(TargetedNightAbility):
    key = "lookout"
    priority = 4

    def apply(self, state, intent, ctx: NightContext):
        state.require_player(intent.target).add_status(StatusType.WATCHED, source=intent.actor)
        ctx.add_event(GameEvent(
            event_type=GameEventType.LOOKOUT_WATCH,
            actor=intent.actor,
            target=intent.target,
            messages={}
        ))
