from .enums import Faction
from .models import GameEvent


class Resolver:
    def resolve_night(self, state):
        events = []

        visits = {}
        roleblocked = set()
        protection_bonus = {}

        for intent in state.queued:
            if intent.target is None:
                continue
            visits.setdefault(intent.target, []).append(intent.actor)

        intents = sorted(state.queued, key=lambda i: (getattr(i, "priority"), i.actor))

        def actor_can_act(intent):
            return state.is_alive(intent.actor) and (intent.actor in roleblocked)

        for intent in intents:
            if intent.target is None:
                continue
            if not state.is_alive(intent.actor):
                continue

            if intent.ability_key == "roleblock":
                if state.is_alive(intent.target):
                    roleblocked.add(intent.target)
            elif intent.ability_key == "protection":
                if not actor_can_act(intent):
                    continue
                if not state.is_alive(intent.actor):
                    continue

                bonus = int(intent.payload.get("defense_bonus", 1))
                protection_bonus[intent.target] = max(protection_bonus.get(intent.target, 0), bonus)
            elif intent.ability_key == "attack":
                if not actor_can_act(intent):
                    continue

                target = state.require_player(intent.target)
                if not target.alive:
                    continue

                power = int(intent.payload.get("power", 1))
                defense = max(target.defense, protection_bonus.get(intent.target, 0))

                if power > defense:
                    target.alive = False
                    events.append(GameEvent(
                        event_type="KILL",
                        actor=intent.actor,
                        target=intent.target,
                        message="Your target has been killed."
                    ))
                else:
                    events.append(GameEvent(
                        event_type="ATTACK_BLOCKED",
                        actor=intent.actor,
                        target=intent.target,
                        message="Your target's defense was too strong!"
                    ))
            elif intent.ability_key == "sheriff":
                if not actor_can_act(intent):
                    continue
                if not state.is_alive(intent.target):
                    continue

                target = state.require_player(intent.target)
                suspicious = (target.role.faction == Faction.MAFIA) or ("framed" in target.status)
                events.append(GameEvent(
                    event_type="SHERIFF_RESULT",
                    actor=intent.actor,
                    target=intent.target,
                    message=("Your target is suspicious.")
                ))

        state.clear_night_state()

        return events
