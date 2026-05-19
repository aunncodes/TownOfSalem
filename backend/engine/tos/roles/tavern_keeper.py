from backend.engine.tos.abilities.tavernkeeper import TavernKeeperAbility
from backend.engine.tos.enums.faction import Faction, SubFaction
from backend.engine.tos.enums.tag import Tag
from backend.engine.tos.models.role import Role, RoleData


class TavernKeeperRole(Role):
    def __init__(self):
        super().__init__(
        key="tavernkeeper",
        name="Tavern Keeper",
        faction=Faction.TOWN,
        subfaction=SubFaction.SUPPORT,
        tags=[Tag.DETECTION_IMMUNE, Tag.ROLEBLOCK_IMMUNE],
        data=RoleData("Your target could be an Tavern Keeper, Transporter, Bootlegger, or Hypnotist."),
        abilities=[TavernKeeperAbility()],
    )