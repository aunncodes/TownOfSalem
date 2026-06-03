from backend.engine.tos.abilities.base import TargetedNightAbility
from backend.engine.tos.enums.game_event import GameEventType
from backend.engine.tos.enums.status import StatusType
from backend.engine.tos.enums.tag import Tag
from backend.engine.tos.models.events import GameEvent
from backend.engine.tos.models.night_context import NightContext


class TavernKeeperAbility(TargetedNightAbility):
    key = "roleblock"
    priority = 2

    def apply(self, state, intent, ctx: NightContext):
        target = state.require_player(intent.target)
        if Tag.ROLEBLOCK_IMMUNE in target.role.tags:
            ctx.add_event(GameEvent(
                event_type=GameEventType.TARGET_ROLEBLOCKED,
                actor=intent.actor,
                target=intent.target,
                messages={intent.target: "Someone tried to role block you but you are immune!"}
            ))
            return

        target.add_status(StatusType.ROLEBLOCKED, source=intent.actor)
        ctx.add_event(GameEvent(
            event_type=GameEventType.TARGET_ROLEBLOCKED,
            actor=intent.actor,
            target=intent.target,
            messages={intent.target: "Someone occupied your night. You were role blocked!"}
        ))
