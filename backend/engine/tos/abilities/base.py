from backend.engine.tos.enums.phase import Phase
from backend.engine.tos.models.action_intent import ActionIntent
from backend.engine.tos.models.night_context import NightContext


class Ability:
    key = ""
    phase = None
    priority = 999
    payload = {}
    requires_target = True
    requires_living_actor = True
    requires_living_target = True
    causes_visit = True

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
        if ctx.is_roleblocked(intent.actor):
            return
        if self.requires_living_target:
            if intent.target is None:
                return
            if not state.is_alive(intent.target):
                return
        if self.causes_visit and intent.target is not None:
            ctx.add_visit(intent.actor, intent.target)

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

class TargetedDayAbility(Ability):
    phase = Phase.DAY

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