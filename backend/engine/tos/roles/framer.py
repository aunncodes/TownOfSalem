from backend.engine.tos.enums.faction import Faction, SubFaction
from backend.engine.tos.models.role import Role, RoleData
from backend.engine.tos.abilities.framer import FramerAbility


class FramerRole(Role):
    def __init__(self):
        super().__init__(
            key="framer",
            name="Framer",
            faction=Faction.MAFIA,
            subfaction=SubFaction.DECEPTION,
            tags=[],
            data=RoleData("Your target could be a Framer, Vampire, or Jester."),
            abilities=[FramerAbility()],
        )
