from backend.engine.tos.abilities.lookout import LookoutAbility
from backend.engine.tos.enums.faction import Faction, SubFaction
from backend.engine.tos.enums.tag import Tag
from backend.engine.tos.models.role import Role, RoleData


class LookoutRole(Role):
    def __init__(self):
        super().__init__(
            key="lookout",
            name="Lookout",
            faction=Faction.TOWN,
            subfaction=SubFaction.INVESTIGATIVE,
            tags=[Tag.DETECTION_IMMUNE],
            data=RoleData("Your target could be a Lookout, Forger, or Witch."),
            abilities=[LookoutAbility()],
        )
