from uuid import uuid4
from backend.engine.tos.manager.game_manager import GameManager


class GameStore:
    def __init__(self):
        self.games: dict[str, GameManager] = {}

    def create_game(self, players) -> tuple[str, GameManager]:
        game_id = uuid4().hex

        manager = GameManager()
        manager.create_game(players)

        self.games[game_id] = manager

        return game_id, manager

    def get_game(self, game_id: str) -> GameManager:
        if game_id not in self.games:
            raise KeyError(f"Unknown game id: {game_id}")

        return self.games[game_id]

    def delete_game(self, game_id: str) -> None:
        if game_id in self.games:
            del self.games[game_id]

    def list_games(self) -> dict[str, GameManager]:
        return dict(self.games)


game_store = GameStore()