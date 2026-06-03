from backend.engine.tos.abilities.base import TargetedNightAbility
from backend.engine.tos.enums.game_event import GameEventType
from backend.engine.tos.enums.status import StatusType
from backend.engine.tos.enums.tag import Tag
from backend.engine.tos.models.events import GameEvent


class SheriffAbility(TargetedNightAbility):
    key = "sheriff"
    priority = 4

    def apply(self, state, intent, ctx):
        target = state.require_player(intent.target)
        suspicious = (Tag.DETECTION_IMMUNE not in target.role.tags) or target.has_status(StatusType.FRAMED) # Detection immune term is a bit vague, but simply all roles that should appear innocent are "Detection immune". Simply implemented like this to match the real game.

        ctx.add_event(GameEvent(
            event_type=GameEventType.SHERIFF_RESULT,
            actor=intent.actor,
            target=intent.target,
            messages={intent.actor: ("Your target is suspicious or framed!" if suspicious else "You cannot find evidence of wrongdoing. Your target is innocent or great at hiding secrets!")}
        ))
