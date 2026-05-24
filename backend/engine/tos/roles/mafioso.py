from backend.engine.tos.abilities.mafioso import MafiosoAbility
from backend.engine.tos.enums.faction import Faction, SubFaction
from backend.engine.tos.models.role import Role, RoleData


class MafiosoRole(Role):
    def __init__(self):
        super().__init__(
            key="mafioso",
            name="Mafioso",
            faction=Faction.MAFIA,
            subfaction=SubFaction.KILLING,
            tags=[],
            data=RoleData("Your target could be a Vigilante, Veteran, Mafioso, or Ambusher."),
            abilities=[MafiosoAbility()],
        )