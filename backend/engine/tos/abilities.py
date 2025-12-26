from .enums import Phase, Tag
from .models import ActionIntent


class Ability:
    key = ""
    phase = None

    def validate(self, state, actor, target):
        raise NotImplementedError

    def create_intent(self, state, actor, target):
        self.validate(state, actor, target)
        return ActionIntent(actor=actor, ability_key=self.key, target=target)


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


class AttackAbility(TargetedNightAbility):
    key = "attack"

    def validate(self, state, actor, target):
        self.require_living_actor(state, actor)
        target_id = self.require_target(state, target)
        if not state.is_alive(target_id):
            raise ValueError("Target is dead")

    def create_intent(self, state, actor, target):
        self.validate(state, actor, target)
        return ActionIntent(actor=actor, ability_key=self.key, target=target, payload={"power": 1})


class InvestigateAbility(TargetedNightAbility):
    key = "investigate"

    def validate(self, state, actor, target):
        self.require_living_actor(state, actor)
        target_id = self.require_target(state, target)
        if not state.is_alive(target_id):
            raise ValueError("Target is dead")


class ProtectAbility(TargetedNightAbility):
    key = "protect"

    def validate(self, state, actor, target):
        self.require_living_actor(state, actor)
        target_id = self.require_target(state, target)
        if not state.is_alive(target_id):
            raise ValueError("Target is dead")

    def create_intent(self, state, actor, target):
        self.validate(state, actor, target)
        return ActionIntent(actor=actor, ability_key=self.key, target=target, payload={"defense_bonus": 1})


class RoleblockAbility(TargetedNightAbility):
    key = "roleblock"

    def validate(self, state, actor, target):
        self.require_living_actor(state, actor)
        target_id = self.require_target(state, target)
        if not state.is_alive(target_id):
            raise ValueError("Target is dead")

        target_player = state.require_player(target_id)
        if Tag.ROLEBLOCK_IMMUNE in target_player.role.tags:
            raise ValueError("Target is roleblock-immune")
