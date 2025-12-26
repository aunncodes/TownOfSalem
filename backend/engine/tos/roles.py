from .abilities import MafiosoAbility, SheriffAbility, DoctorAbility, TavernKeeperAbility
from .enums import Faction, Tag, SubFaction
from .models import Role


ROLE_REGISTRY = {
    "mafioso": Role(
        key="mafioso",
        name="Mafioso",
        faction=Faction.MAFIA,
        subfaction=SubFaction.KILLING,
        tags=[],
        abilities=[MafiosoAbility()],
    ),
    "sheriff": Role(
        key="sheriff",
        name="Sheriff",
        faction=Faction.TOWN,
        subfaction=SubFaction.INVESTIGATIVE,
        tags=[],
        abilities=[SheriffAbility()],
    ),
    "doctor": Role(
        key="doctor",
        name="Doctor",
        faction=Faction.TOWN,
        subfaction=SubFaction.PROTECTIVE,
        tags=[],
        abilities=[DoctorAbility()],
    ),
    "tavernkeeper": Role(
        key="tavernkeeper",
        name="Tavern Keeper",
        faction=Faction.TOWN,
        subfaction=SubFaction.SUPPORT,
        tags=[],
        abilities=[TavernKeeperAbility()],
    ),
}
