from backend.engine.tos.abilities.veteran import VeteranAbility
from backend.engine.tos.enums.faction import SubFaction, Faction
from backend.engine.tos.enums.tag import Tag
from backend.engine.tos.models.role import Role, RoleData


class VeteranRole(Role):
    def __init__(self):
        super().__init__(
            key="veteran",
            name="Veteran",
            faction=Faction.TOWN,
            subfaction=SubFaction.KILLING,
            tags=[Tag.DETECTION_IMMUNE],
            data=RoleData("Your target could be a Vigilante, Veteran, Mafioso, or Ambusher."),
            abilities=[VeteranAbility()],
        )