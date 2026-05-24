from backend.engine.tos.enums.game_event import GameEventType
from backend.engine.tos.enums.phase import Phase
from backend.engine.tos.enums.status import Status
from backend.engine.tos.enums.tag import Tag
from backend.engine.tos.models.action_intent import ActionIntent
from backend.engine.tos.models.day_context import DayContext
from backend.engine.tos.models.events import GameEvent
from backend.engine.tos.models.night_context import NightContext


class Ability:
    key = ""
    phase = None
    priority = 999
    requires_target = False
    requires_living_actor = False
    requires_living_target = False
    causes_visit = False

    def create_intent(self, state, actor, target):
        return ActionIntent(
            actor=actor,
            ability_key=self.key,
            target=target,
            priority=self.priority,
        )

    def resolve_intent(self, state, intent, ctx):
        if self.requires_target and intent.target is None:
            return

        if self.requires_living_actor and not state.is_alive(intent.actor):
            return

        if self.requires_living_target:
            if intent.target is None:
                return
            if not state.is_alive(intent.target):
                return

        self.apply(state, intent, ctx)

    def apply(self, state, intent, ctx):
        raise NotImplementedError()

class NightAbility(Ability):
    phase = Phase.NIGHT

    requires_target = False
    requires_living_actor = True
    requires_living_target = False
    causes_visit = False

    def resolve_intent(self, state, intent, ctx: NightContext):
        if self.requires_target and intent.target is None:
            return

        if self.requires_living_actor and not state.is_alive(intent.actor):
            return

        if Status.JAILED in state.require_player(intent.actor).status:
            return

        if Status.ROLEBLOCKED in state.require_player(intent.actor).status:
            return

        if self.requires_living_target:
            if intent.target is None:
                return
            if not state.is_alive(intent.target):
                return

        if intent.target is not None and Status.JAILED in state.require_player(intent.target).status and Tag.JAILED_IMMUNE not in state.require_player(intent.actor).role.tags: # TODO: Fix not checking if this is the correlating Jailor
            ctx.add_event(GameEvent(
                event_type=GameEventType.TARGET_JAILED,
                actor=intent.actor,
                target=intent.target,
                messages={intent.actor: "Your ability failed because your target was in jail."}
            ))
            return

        if intent.target is not None and Status.ALERT in state.require_player(intent.target).status:
            ctx.add_event(GameEvent(
                event_type=GameEventType.VETERAN_SHOT,
                actor=intent.target,
                target=intent.actor,
                messages={intent.target: "You shot someone who visited you last night!", intent.actor: "You were shot by the Veteran you visited!"}
            ))
            defense = max(state.require_player(intent.actor).defense, ctx.get_protection_bonus(intent.actor))
            if defense < 2:
                state.require_player(intent.actor).alive = False # Doesn't return since ability actually still happens

        if self.causes_visit and intent.target is not None:
            ctx.add_visit(intent.actor, intent.target)

        self.apply(state, intent, ctx)

class TargetedNightAbility(NightAbility):
    requires_target = True
    requires_living_actor = True
    requires_living_target = True
    causes_visit = True

class TargetedDayAbility(Ability):
    requires_target = True
    requires_living_actor = True
    requires_living_target = True
    phase = Phase.DAY

    def apply(self, state, intent, ctx: DayContext):
        raise NotImplementedError()