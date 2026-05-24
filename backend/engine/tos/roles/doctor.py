from backend.engine.tos.abilities.doctor import DoctorAbility
from backend.engine.tos.enums.faction import SubFaction, Faction
from backend.engine.tos.enums.tag import Tag
from backend.engine.tos.models.role import Role, RoleData


class DoctorRole(Role):
    def __init__(self):
        super().__init__(
            key="doctor",
            name="Doctor",
            faction=Faction.TOWN,
            subfaction=SubFaction.PROTECTIVE,
            tags=[Tag.DETECTION_IMMUNE],
            data=RoleData("Your target could be a Doctor, Disguiser, or Serial Killer."),
            abilities=[DoctorAbility()],
        )