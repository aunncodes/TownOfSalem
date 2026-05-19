from backend.engine.tos.abilities.jailor import JailorDayAbility, JailorExecuteAbility
from backend.engine.tos.enums.faction import SubFaction, Faction
from backend.engine.tos.enums.tag import Tag
from backend.engine.tos.models.role import Role, RoleData


class JailorRole(Role):
    def __init__(self):
        super().__init__(
        key="jailor",
        name="Joctor",
        faction=Faction.TOWN,
        subfaction=SubFaction.KILLING,
        tags=[Tag.DETECTION_IMMUNE],
        data=RoleData("Your target could be a Spy, Blackmailer, or Jailor."),
        abilities=[JailorDayAbility(), JailorExecuteAbility],
    )