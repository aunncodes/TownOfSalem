from .abilities import MafiosoAbility, SheriffAbility, DoctorAbility, TavernKeeperAbility, InvestigatorAbility
from .enums import Faction, Tag, SubFaction
from .models import Role, RoleData

ROLE_REGISTRY = {
    "mafioso": Role(
        key="mafioso",
        name="Mafioso",
        faction=Faction.MAFIA,
        subfaction=SubFaction.KILLING,
        tags=[],
        data=RoleData("Your target could be a Vigilante, Veteran, Mafioso, or Ambusher."),
        abilities=[MafiosoAbility()],
    ),
    "sheriff": Role(
        key="sheriff",
        name="Sheriff",
        faction=Faction.TOWN,
        subfaction=SubFaction.INVESTIGATIVE,
        tags=[Tag.DETECTION_IMMUNE],
        data=RoleData("Your target could be a Sheriff, Executioner, or Werewolf."),
        abilities=[SheriffAbility()],
    ),
    "doctor": Role(
        key="doctor",
        name="Doctor",
        faction=Faction.TOWN,
        subfaction=SubFaction.PROTECTIVE,
        tags=[Tag.DETECTION_IMMUNE],
        data=RoleData("Your target could be a Doctor, Disguiser, or Serial Killer."),
        abilities=[DoctorAbility()],
    ),
    "tavernkeeper": Role(
        key="tavernkeeper",
        name="Tavern Keeper",
        faction=Faction.TOWN,
        subfaction=SubFaction.SUPPORT,
        tags=[Tag.DETECTION_IMMUNE],
        data=RoleData("Your target could be an Tavern Keeper, Transporter, Bootlegger, or Hypnotist."),
        abilities=[TavernKeeperAbility()],
    ),
    "investigator": Role(
        key="investigator",
        name="Investigator",
        faction=Faction.TOWN,
        subfaction=SubFaction.INVESTIGATIVE,
        tags=[Tag.DETECTION_IMMUNE],
        data=RoleData("Your target could be an Investigator, Consigliere, or Mayor."),
        abilities=[InvestigatorAbility()],
    )
}
