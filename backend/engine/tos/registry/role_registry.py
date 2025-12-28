from backend.engine.tos.roles.doctor import DoctorRole
from backend.engine.tos.roles.investigator import InvestigatorRole
from backend.engine.tos.roles.mafioso import MafiosoRole
from backend.engine.tos.roles.sheriff import SheriffRole
from backend.engine.tos.roles.tavern_keeper import TavernKeeperRole

ROLE_REGISTRY = {
    "mafioso": MafiosoRole(),
    "sheriff": SheriffRole(),
    "doctor": DoctorRole(),
    "tavernkeeper": TavernKeeperRole(),
    "investigator": InvestigatorRole()
}
