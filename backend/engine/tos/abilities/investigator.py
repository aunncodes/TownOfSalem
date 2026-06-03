from backend.engine.tos.abilities.base import TargetedNightAbility
from backend.engine.tos.enums.game_event import GameEventType
from backend.engine.tos.models.events import GameEvent
from backend.engine.tos.models.night_context import NightContext
from backend.engine.tos.enums.status import StatusType


class InvestigatorAbility(TargetedNightAbility):
    key = "investigator"
    priority = 4

    def apply(self, state, intent, ctx: NightContext):
        target = state.require_player(intent.target)
        framed = target.get_statuses(StatusType.FRAMED)
        result = target.role.data.investigator_result if len(framed) == 0 else "Your target could be a Framer, Vampire, or Jester." # TODO: Probably shouldn't be hardcoded
        for status in framed:
            status.data["checked"] = True # checks all framed events
        ctx.add_event(GameEvent(
            event_type=GameEventType.INVESTIGATION_RESULT,
            actor=intent.actor,
            target=intent.target,
            messages={intent.actor: result}
        ))
