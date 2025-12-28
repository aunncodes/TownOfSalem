from backend.engine.tos.abilities.base import TargetedNightAbility
from backend.engine.tos.enums.game_event import GameEventType
from backend.engine.tos.models.events import GameEvent
from backend.engine.tos.models.night_context import NightContext


class InvestigatorAbility(TargetedNightAbility):
    key = "investigator"
    priority = 4

    def apply(self, state, intent, ctx: NightContext):
        target = state.require_player(intent.target)
        ctx.add_event(GameEvent(
            event_type=GameEventType.INVESTIGATION_RESULT,
            actor=intent.actor,
            target=intent.target,
            message=target.role.data.investigator_result
        ))