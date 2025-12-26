from .enums import Faction, GameEventType, Tag
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

        for intent in intents:
            if intent.target is None:
                continue
            if not state.is_alive(intent.actor):
                continue

            if intent.ability_key == "roleblock":
                target = state.require_player(intent.target)
                if not state.is_alive(intent.actor):
                    continue
                if Tag.ROLEBLOCK_IMMUNE in target.role.tags:
                    events.append(GameEvent(
                        event_type=GameEventType.TARGET_ROLEBLOCKED,
                        actor=intent.actor,
                        target=intent.target,
                        target_message="Someone tried to role block you but you are immune!"
                    ))
                    continue

                roleblocked.add(intent.target)
                events.append(GameEvent(
                    event_type=GameEventType.TARGET_ROLEBLOCKED,
                    actor=intent.actor,
                    target=intent.target,
                    target_message="Someone occupied your night. You were role blocked!"
                ))
            elif intent.ability_key == "protection":
                if not state.is_alive(intent.actor):
                    continue
                target = state.require_player(intent.target)
                if not target.alive:
                    continue

                bonus = int(intent.payload.get("defense_bonus", 1))
                protection_bonus[target] = max(protection_bonus.get(target, 0), bonus)
            elif intent.ability_key == "attack":
                target = state.require_player(intent.target)
                if not target.alive:
                    continue

                power = int(intent.payload.get("power", 1))
                defense = max(target.defense, protection_bonus.get(intent.target, 0))

                if power > defense:
                    target.alive = False
                    events.append(GameEvent(
                        event_type=GameEventType.KILL,
                        actor=intent.actor,
                        target=intent.target,
                        target_message="You were attacked by a member of the Mafia!"
                    ))
                else:
                    events.append(GameEvent(
                        event_type=GameEventType.ATTACK_BLOCKED,
                        actor=intent.actor,
                        target=intent.target,
                        message="Your target's defense was too strong to kill.",
                        target_message="You were attacked by a member of the Mafia!"
                    ))
            elif intent.ability_key == "sheriff":
                if not state.is_alive(intent.target):
                    continue

                target = state.require_player(intent.target)
                suspicious = (not Tag.DETECTION_IMMUNE in target.role.tags) or ("framed" in target.status)

                events.append(GameEvent(
                    event_type="SHERIFF_RESULT",
                    actor=intent.actor,
                    target=intent.target,
                    message=("Your target is suspicious or framed!" if suspicious else "You cannot find evidence of wrongdoing. Your target is innocent or great at hiding secrets!")
                ))
            elif intent.ability_key == "investigator":
                if not state.is_alive(intent.actor):
                    continue
                target = state.require_player(intent.target)
                events.append(GameEvent(
                    event_type=GameEventType.INVESTIGATION_RESULT,
                    actor=intent.actor,
                    target=intent.target,
                    message=target.data.investigator_result
                ))

        state.queued.clear()

        return events
