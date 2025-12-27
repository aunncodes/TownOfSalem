from .enums import Phase, Tag, GameEventType
from .models import ActionIntent, NightContext, GameEvent


class Ability:
    key = ""
    phase = None
    priority = 999
    payload = {}
    requires_target = True
    requires_living_actor = True
    requires_living_target = True
    blocked_by_roleblock = True

    def validate(self, state, actor, target):
        raise NotImplementedError

    def build_payload(self, state, actor, target):
        return dict(self.payload)

    def create_intent(self, state, actor, target):
        self.validate(state, actor, target)
        return ActionIntent(actor=actor, ability_key=self.key, target=target, payload=self.build_payload(state, actor, target), priority=self.priority)

    def resolve_intent(self, state, intent, ctx: NightContext):
        if self.requires_target and intent.target is None:
            return
        if self.requires_living_actor and not state.is_alive(intent.actor):
            return
        if self.blocked_by_roleblock and ctx.is_roleblocked(intent.actor):
            return
        if self.requires_living_target:
            if intent.target is None:
                return
            if not state.is_alive(intent.target):
                return

        self.apply(state, intent, ctx)

    def apply(self, state, intent, ctx: NightContext):
        return

class TargetedNightAbility(Ability):
    phase = Phase.NIGHT

    def require_target(self, state, target):
        if target is None:
            raise ValueError("Target required")
        state.require_player(target)
        return target

    def require_living_actor(self, state, actor):
        state.require_player(actor)
        if not state.is_alive(actor):
            raise ValueError("Dead players cannot act")

    def validate(self, state, actor, target):
        self.require_living_actor(state, actor)
        target_id = self.require_target(state, target)
        if not state.is_alive(target_id):
            raise ValueError("Target is dead")


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
                target_message="You were attacked by a member of the Mafia!"
            ))

class SheriffAbility(TargetedNightAbility):
    key = "sheriff"
    priority = 4

    def apply(self, state, intent, ctx):
        target = state.require_player(intent.target)
        suspicious = (Tag.DETECTION_IMMUNE not in target.role.tags) or ("framed" in target.status)

        ctx.add_event(GameEvent(
            event_type=GameEventType.SHERIFF_RESULT,
            actor=intent.actor,
            target=intent.target,
            message=("Your target is suspicious or framed!" if suspicious else "You cannot find evidence of wrongdoing. Your target is innocent or great at hiding secrets!")
        ))
class DoctorAbility(TargetedNightAbility):
    key = "protect"
    priority = 3
    payload = {"defense_bonus": 1}

    def apply(self, state, intent, ctx):
        bonus = int(intent.payload.get("defense_bonus", 1))
        ctx.add_protection(intent.target, bonus)

class InvestigatorAbility(TargetedNightAbility):
    key = "investigator"
    priority = 4

    def apply(self, state, intent, ctx: NightContext):
        target = state.require_player(intent.target)
        ctx.add_event(GameEvent(
            event_type=GameEventType.INVESTIGATION_RESULT,
            actor=intent.actor,
            target=intent.target,
            message=target.role.data.investigator_result
        ))

class TavernKeeperAbility(TargetedNightAbility):
    key = "roleblock"
    priority = 2

    def apply(self, state, intent, ctx: NightContext):
        target = state.require_player(intent.target)
        if Tag.ROLEBLOCK_IMMUNE in target.role.tags:
            ctx.add_event(GameEvent(
                event_type=GameEventType.TARGET_ROLEBLOCKED,
                actor=intent.actor,
                target=target,
                target_message="Someone tried to role block you but you are immune!"
            ))
            return

        ctx.roleblocked.add(intent.target)
        ctx.add_event(GameEvent(
            event_type=GameEventType.TARGET_ROLEBLOCKED,
            actor=intent.actor,
            target=target,
            target_message="Someone occupied your night. You were role blocked!"
        ))