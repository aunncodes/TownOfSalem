from .enums import Phase, Tag
from .models import ActionIntent


class Ability:
    key = ""
    phase = None
    priority = 999
    default_payload = {}

    def validate(self, state, actor, target):
        raise NotImplementedError

    def build_payload(self, state, actor, target):
        return dict(self.default_payload)

    def create_intent(self, state, actor, target):
        self.validate(state, actor, target)
        return ActionIntent(actor=actor, ability_key=self.key, target=target, payload=self.build_payload(state, actor, target), priority=self.priority)


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
    default_payload = {"power": 1}

class SheriffAbility(TargetedNightAbility):
    key = "sheriff"
    priority = 4

class DoctorAbility(TargetedNightAbility):
    key = "protect"
    priority = 3
    default_payload = {"defense_bonus": 1}

class InvestigatorAbility(TargetedNightAbility):
    key = "investigator"
    priority = 4

class TavernKeeperAbility(TargetedNightAbility):
    key = "roleblock"
    priority = 2