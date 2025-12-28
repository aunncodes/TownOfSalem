from backend.engine.tos.models import NightContext


class Resolver:
    def __init__(self, role_registry):
        self.ability_by_key = {}
        for role in role_registry.values():
            for ability in role.abilities:
                self.ability_by_key[ability.key] = ability

    def resolve_night(self, state):
        ctx = NightContext()

        intents = sorted(state.queued, key=lambda i: (getattr(i, "priority", 999), int(i.actor)))

        for intent in intents:
            if intent.target is None:
                continue
            if not state.is_alive(intent.actor):
                continue

            ability = self.ability_by_key.get(intent.ability_key)
            if ability is None:
                continue

            ability.resolve_intent(state, intent, ctx)

        state.queued.clear()
        return ctx.events
