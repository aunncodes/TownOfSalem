from backend.engine.tos.enums.game_event import GameEventType
from backend.engine.tos.enums.status import StatusType
from backend.engine.tos.models.day_context import DayContext
from backend.engine.tos.models.events import GameEvent
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

    def resolve_lookout_events(self, state, ctx):
        for watched_id, player in state.players.items():
            watched_statuses = player.get_statuses(StatusType.WATCHED)
            if len(watched_statuses) == 0:
                continue

            for status in watched_statuses:
                visitors = [visitor for visitor in ctx.get_visits(watched_id) if visitor != status.source]
                for visitor in visitors[:3]:
                    ctx.add_event(GameEvent(
                        event_type=GameEventType.LOOKOUT_SAW,
                        actor=status.source,
                        target=watched_id,
                        messages={status.source: f"{state.require_player(visitor).name} visited your target last night!"}
                    ))
                if len(visitors) > 3:
                    ctx.add_event(GameEvent(
                        event_type=GameEventType.LOOKOUT_SAW,
                        actor=status.source,
                        messages={status.source: "More people visited your target but you couldn't identify them."}
                    ))

    def resolve_night(self, state):
        ctx = NightContext()
        self.resolve_intents(state, ctx)
        self.resolve_lookout_events(state, ctx)
        return ctx.events
