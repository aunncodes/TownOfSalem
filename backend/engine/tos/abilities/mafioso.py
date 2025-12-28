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
        defense = max(target.defense, ctx.get_protection_bonus(intent.target))

        if power > defense:
            target.alive = False
            ctx.add_event(GameEvent(
                event_type=GameEventType.KILL,
                actor=intent.actor,
                target=intent.target,
                target_message="You were attacked by a member of the Mafia!"
            ))
        else:
            ctx.add_event(GameEvent(
                event_type=GameEventType.ATTACK_BLOCKED,
                actor=intent.actor,
                target=intent.target,
                message="Your target's defense was too strong to kill.",
                target_message="Someone attacked you but your defense was too strong!" # TODO: should detect if protection was the reason, too lazy to do that rn
            ))