from .abilities import AttackAbility, InvestigateAbility, ProtectAbility, RoleblockAbility
from .enums import Faction, Tag
from .models import Role


ROLE_REGISTRY = {
    "mafioso": Role(
        key="mafioso",
        name="Mafioso",
        faction=Faction.MAFIA,
        tags=[Tag.KILLING],
        abilities=[AttackAbility()],
    ),
    "sheriff": Role(
        key="sheriff",
        name="Sheriff",
        faction=Faction.TOWN,
        tags=[Tag.INVESTIGATIVE],
        abilities=[InvestigateAbility()],
    ),
    "doctor": Role(
        key="doctor",
        name="Doctor",
        faction=Faction.TOWN,
        tags=[Tag.PROTECTIVE],
        abilities=[ProtectAbility()],
    ),
    "tavernkeeper": Role(
        key="tavernkeeper",
        name="Tavern Keeper",
        faction=Faction.TOWN,
        tags=[],
        abilities=[RoleblockAbility()],
    ),
}
