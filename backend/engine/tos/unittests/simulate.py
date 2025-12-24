from backend.engine.tos.core.Player import Player
from backend.engine.tos.roles.mafioso import Mafioso
from backend.engine.tos.roles.sheriff import Sheriff

players = [Player(Sheriff(), "A"), Player(Mafioso(), "B")]

print(players[0].getRole().action(players[1]))
print(players[1].getRole().action(players[0]))