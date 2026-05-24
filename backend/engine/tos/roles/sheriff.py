from backend.engine.tos.abilities.sheriff import SheriffAbility
from backend.engine.tos.enums.faction import Faction, SubFaction
from backend.engine.tos.enums.tag import Tag
from backend.engine.tos.models.role import Role, RoleData


class SheriffRole(Role):
    def __init__(self):
        super().__init__(
            key="sheriff",
            name="Sheriff",
            faction=Faction.TOWN,
            subfaction=SubFaction.INVESTIGATIVE,
            tags=[Tag.DETECTION_IMMUNE],
            data=RoleData("Your target could be a Sheriff, Executioner, or Werewolf."),
            abilities=[SheriffAbility()],
        )