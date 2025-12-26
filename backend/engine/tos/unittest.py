from backend.engine.tos.enums import Phase
from backend.engine.tos.models import GameState, Player
from backend.engine.tos.roles import ROLE_REGISTRY

state = GameState(Phase.NIGHT, [Player(0, "Player 1", ROLE_REGISTRY["sheriff"]), Player(1, "Player 2", ROLE_REGISTRY["mafioso"])])
