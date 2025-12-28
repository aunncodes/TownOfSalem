from backend.engine.tos.abilities.base import TargetedNightAbility
from backend.engine.tos.enums.game_event import GameEventType
from backend.engine.tos.enums.status import Status
from backend.engine.tos.enums.tag import Tag
from backend.engine.tos.models.events import GameEvent


class SheriffAbility(TargetedNightAbility):
    key = "sheriff"
    priority = 4

    def apply(self, state, intent, ctx):
        target = state.require_player(intent.target)
        suspicious = (Tag.DETECTION_IMMUNE not in target.role.tags) or (Status.FRAMED in target.status)

        ctx.add_event(GameEvent(
            event_type=GameEventType.SHERIFF_RESULT,
            actor=intent.actor,
            target=intent.target,
            message=("Your target is suspicious or framed!" if suspicious else "You cannot find evidence of wrongdoing. Your target is innocent or great at hiding secrets!")
        ))