from backend.engine.tos.abilities.base import TargetedDayAbility, TargetedNightAbility
from backend.engine.tos.enums.game_event import GameEventType
from backend.engine.tos.enums.status import StatusType
from backend.engine.tos.models.events import GameEvent


class JailorDayAbility(TargetedDayAbility):
    key = "jailorselect"
    priority = 1

    def apply(self, state, intent, ctx):
        target = state.require_player(intent.target)

        target.add_status(StatusType.JAILED, source=intent.actor)

        ctx.add_event(GameEvent(
            event_type=GameEventType.JAIL_SELECTED,
            actor=intent.actor,
            target=target.id,
            messages={intent.actor: "You dragged your target off to jail!", intent.target: "You were hauled off to jail!"}
        ))


class JailorExecuteAbility(TargetedNightAbility):
    key = "execute"
    priority = 3

    def apply(self, state, intent, ctx):
        target = state.require_player(intent.target)

        if not target.has_status(StatusType.JAILED):
            return

        defense = max(target.defense, ctx.get_protection_bonus(intent.target))
        if defense < 3:
            target.alive = False

        ctx.add_event(GameEvent(
            event_type=GameEventType.KILL,
            actor=intent.actor,
            target=intent.target,
            messages={
                intent.actor: f"You executed {target.name}.",
                intent.target: "You were executed by the Jailor!"
            }
        ))
