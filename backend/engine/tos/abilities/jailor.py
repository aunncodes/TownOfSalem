from backend.engine.tos.abilities.base import TargetedDayAbility, TargetedNightAbility
from backend.engine.tos.enums.game_event import GameEventType
from backend.engine.tos.models.events import GameEvent


class JailorDayAbility(TargetedDayAbility):
    key = "jailorselect"
    priority = 1

    def apply(self, state, intent, ctx):
        target = state.require_player(intent.target)

        ctx.select_jail_target(intent.actor, target.id)

        ctx.add_event(GameEvent(
            event_type=GameEventType.JAIL_SELECTED,
            actor=intent.actor,
            target=target.id,
            messages={intent.actor: f"You dragged your target off to jail!", intent.target: "You were hauled off to jail!"}
        ))


class JailorExecuteAbility(TargetedNightAbility):
    key = "execute"
    priority = 3
    payload = {"power": 3}

    def validate(self, state, actor, target):
        self.require_living_actor(state, actor)
        target_id = self.require_target(state, target)

        if not state.is_alive(target_id):
            raise ValueError("Target is dead")

    def apply(self, state, intent, ctx):
        target = state.require_player(intent.target)

        jailed_target = ctx.get_jailed_target_for(intent.actor)

        if jailed_target != intent.target:
            return

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