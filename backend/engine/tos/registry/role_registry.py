from backend.engine.tos.roles.doctor import DoctorRole
from backend.engine.tos.roles.investigator import InvestigatorRole
from backend.engine.tos.roles.jailor import JailorRole
from backend.engine.tos.roles.lookout import LookoutRole
from backend.engine.tos.roles.mafioso import MafiosoRole
from backend.engine.tos.roles.sheriff import SheriffRole
from backend.engine.tos.roles.tavern_keeper import TavernKeeperRole
from backend.engine.tos.roles.veteran import VeteranRole


ROLE_REGISTRY = {
    "mafioso": MafiosoRole,
    "sheriff": SheriffRole,
    "doctor": DoctorRole,
    "tavernkeeper": TavernKeeperRole,
    "investigator": InvestigatorRole,
    "jailor": JailorRole,
    "lookout": LookoutRole,
    "veteran": VeteranRole,
}
