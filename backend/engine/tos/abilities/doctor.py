from backend.engine.tos.abilities.base import TargetedNightAbility
from backend.engine.tos.models.night_context import NightContext


class DoctorAbility(TargetedNightAbility):
    key = "protect"
    priority = 3
    payload = {"defense_bonus": 1}

    def apply(self, state, intent, ctx: NightContext):
        bonus = int(intent.payload.get("defense_bonus", 1))
        ctx.add_protection(intent.target, bonus)