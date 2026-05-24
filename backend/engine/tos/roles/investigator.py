from backend.engine.tos.abilities.investigator import InvestigatorAbility
from backend.engine.tos.enums.faction import Faction, SubFaction
from backend.engine.tos.enums.tag import Tag
from backend.engine.tos.models.role import Role, RoleData


class InvestigatorRole(Role):
    def __init__(self):
        super().__init__(
            key="investigator",
            name="Investigator",
            faction=Faction.TOWN,
            subfaction=SubFaction.INVESTIGATIVE,
            tags=[Tag.DETECTION_IMMUNE],
            data=RoleData("Your target could be an Investigator, Consigliere, or Mayor."),
            abilities=[InvestigatorAbility()],
        )