from backend.engine.tos.core.resolver import Resolver
from backend.engine.tos.enums.phase import Phase
from backend.engine.tos.models.action import ActionChoice
from backend.engine.tos.models.events import GameState
from backend.engine.tos.models.player import Player
from backend.engine.tos.registry.role_registry import ROLE_REGISTRY


class GameManager:
    def __init__(self, role_registry=ROLE_REGISTRY):
        self.role_registry = role_registry
        self.resolver = Resolver(role_registry)
        self.state = None

    def create_game(self, players):
        self.state = GameState(
            phase=Phase.DAY,
            players={
                pid: Player(
                    pid=pid,
                    name=data["name"],
                    role=self.role_registry[data["role"]],
                )
                for pid, data in players.items()
            }
        )

    def require_state(self):
        if self.state is None:
            raise ValueError("Game has not been created")
        return self.state

    def get_players(self):
        return self.require_state().players

    def get_alive_players(self):
        state = self.require_state()

        return {
            pid: player for pid, player in state.players.items() if player.alive
        }

    def get_valid_targets(self, actor):
        state = self.require_state()

        return {
            pid: player for pid, player in state.players.items() if pid != actor and player.alive
        }

    def get_action_choices(self, actor):
        state = self.require_state()
        player = state.require_player(actor)

        choices = []

        if not player.alive:
            return choices

        for ability in player.role.abilities:
            if ability.phase != state.phase:
                continue

            choices.append(ActionChoice(
                name=ability.key,
                actor=actor,
                phase=ability.phase,
                requires_target=ability.requires_target,
                description=None,
            ))

        return choices

    def submit_action(self, actor, ability_key, target=None):
        state = self.require_state()
        player = state.require_player(actor)

        for ability in player.role.abilities:
            if ability.name != ability_key:
                continue

            if ability.phase != state.phase:
                raise ValueError("Ability cannot be used during this phase")

            intent = ability.create_intent(state, actor, target)
            state.queue_intent(intent)
            return intent

        raise ValueError("Player does not have that ability")

    def resolve_phase(self):
        state = self.require_state()

        if state.phase == Phase.DAY:
            return self.resolver.resolve_day(state)

        if state.phase == Phase.NIGHT:
            return self.resolver.resolve_night(state)

        raise ValueError("Unknown phase")

    def advance_phase(self):
        state = self.require_state()
        state.clear_queue()

        state.phase = Phase.DAY if state.phase == Phase.NIGHT else Phase.NIGHT

    def is_game_over(self):
        alive_players = self.get_alive_players()

        factions = set()

        for player in alive_players.values():
            factions.add(player.role.faction)

        return len(factions) <= 1

    def get_winner(self):
        if not self.is_game_over():
            return None

        alive_players = self.get_alive_players()

        if len(alive_players) == 0:
            return None

        for player in alive_players.values():
            return player.role.faction

        return ValueError("If this ever runs, I commend you")