from backend.engine.tos.models.night_context import NightContext


class Resolver:
    def __init__(self, role_registry):
        self.abilities = {}
        for role in role_registry.values():
            for ability in role.abilities:
                self.abilities[ability.key] = ability

    def resolve_night(self, state):
        ctx = NightContext()

        intents = sorted(state.queued, key=lambda i: (getattr(i, "priority", 999), int(i.actor)))

        for intent in intents:
            if intent.target is None:
                continue
            if not state.is_alive(intent.actor):
                continue

            ability = self.abilities.get(intent.ability_key)
            if ability is None:
                continue

            ability.resolve_intent(state, intent, ctx)

        state.queued.clear()
        return ctx.events
