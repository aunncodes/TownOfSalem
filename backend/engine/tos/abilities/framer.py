from backend.engine.tos.abilities.base import TargetedNightAbility
from backend.engine.tos.models.night_context import NightContext
from backend.engine.tos.enums.status import StatusType


def framer_expired(state, data):
    return False # TODO: Should be marked for deletion at the end of the night by sheriff and investigator to account for multiple checks

class FramerAbility(TargetedNightAbility):
    key = "frame"
    priority = 3

    def apply(self, state, intent, ctx: NightContext):
        target = state.require_player(intent.target)
        target.add_status(StatusType.FRAMED, source=intent.actor, expiry=framer_expired)