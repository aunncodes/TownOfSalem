from backend.engine.tos.models.day_context import DayContext
from backend.engine.tos.models.night_context import NightContext


class Resolver:
    def resolve_intents(self, state, ctx):
        intents = sorted(state.queued, key=lambda i: (getattr(i, "priority", 999), int(i.actor)))

        for intent in intents:
            actor = state.require_player(intent.actor)
            ability = None

            for role_ability in actor.role.abilities:
                if role_ability.key == intent.ability_key:
                    ability = role_ability
                    break

            if ability is None:
                continue

            ability.resolve_intent(state, intent, ctx)

        state.queued.clear()

    def resolve_day(self, state):
        ctx = DayContext()
        self.resolve_intents(state, ctx)
        return ctx.events

    def resolve_night(self, state):
        ctx = NightContext()
        self.resolve_intents(state, ctx)
        return ctx.events