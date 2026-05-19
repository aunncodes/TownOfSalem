from backend.engine.tos.abilities.base import TargetedNightAbility
from backend.engine.tos.enums.game_event import GameEventType
from backend.engine.tos.models.events import GameEvent


class MafiosoAbility(TargetedNightAbility):
    key = "attack"
    priority = 5
    payload = {"power": 1}

    def apply(self, state, intent, ctx):
        target = state.require_player(intent.target)

        power = int(intent.payload.get("power", 1))
        defense = target.defense
        protection_bonus = ctx.get_protection_bonus(intent.target)

        if power > defense and power > protection_bonus:
            target.alive = False
            ctx.add_event(GameEvent(
                event_type=GameEventType.KILL,
                actor=intent.actor,
                target=intent.target,
                messages={intent.target: "You were attacked by a member of the Mafia!"}
            ))
        else:
            if power > defense:
                ctx.add_event(GameEvent(
                    event_type=GameEventType.ATTACK_BLOCKED,
                    actor=intent.actor,
                    target=intent.target,
                    messages={intent.actor: "Your target's defense was too strong to kill.", intent.target: "Someone attacked you but your defense was too strong!"}
                ))
            else:
                ctx.add_event(GameEvent(
                    event_type=GameEventType.ATTACK_BLOCKED,
                    actor=intent.actor,
                    target=intent.target,
                    messages={intent.actor: "Your target's defense was too strong to kill.", intent.target: "You were attacked but someone nursed you back to health!"} # TODO: if i add bodyguard, it will need its own flag
                ))