from .enums import Faction
from .models import GameEvent


class Resolver:
    def resolve_night(self, state):
        events = []

        visits_by_target = {}
        roleblocked = set()
        protection_bonus = {}

        for intent in state.queued:
            if intent.target is None:
                continue
            visits_by_target.setdefault(intent.target, []).append(intent.actor)

        for intent in state.queued:
            if intent.ability_key != "roleblock":
                continue
            if intent.target is None:
                continue
            if not state.is_alive(intent.actor):
                continue
            roleblocked.add(intent.target)

        for intent in state.queued:
            if intent.ability_key != "protect":
                continue
            if intent.target is None:
                continue
            if intent.actor in roleblocked:
                continue
            if not state.is_alive(intent.actor):
                continue

            bonus = intent.payload.get("defense_bonus", 1)
            protection_bonus[intent.target] = protection_bonus.get(intent.target, 0) + int(bonus)

        for intent in state.queued:
            if intent.ability_key != "attack":
                continue
            if intent.target is None:
                continue
            if intent.actor in roleblocked:
                continue
            if not state.is_alive(intent.actor):
                continue

            target_id = intent.target
            target = state.require_player(target_id)
            if not target.alive:
                continue

            power = int(intent.payload.get("power", 1))
            defense = target.defense + protection_bonus.get(target_id, 0)

            if power > defense:
                target.alive = False
                events.append(GameEvent(
                    event_type="KILL",
                    actor=intent.actor,
                    target=target_id,
                    message="Your target has been killed."
                ))
            else:
                events.append(GameEvent(
                    event_type="ATTACK_BLOCKED",
                    actor=intent.actor,
                    target=target_id,
                    message="Your target's defense was too strong!"
                ))

        for intent in state.queued:
            if intent.ability_key != "investigate":
                continue
            if intent.target is None:
                continue
            if intent.actor in roleblocked:
                continue
            if not state.is_alive(intent.actor):
                continue

            target = state.require_player(intent.target)
            suspicious = (target.role.faction == Faction.MAFIA) or ("framed" in target.status)

            events.append(GameEvent(
                event_type="INVESTIGATE_RESULT",
                actor=intent.actor,
                target=intent.target,
                message=("Your target is suspicious or framed!" if suspicious else "Your target seems innocent.")
            ))

        state.visits_by_target = visits_by_target
        state.roleblocked = roleblocked
        state.protection_bonus = protection_bonus

        state.queued.clear()
        state.roleblocked.clear()
        state.protection_bonus.clear()
        state.visits_by_target.clear()

        return events
