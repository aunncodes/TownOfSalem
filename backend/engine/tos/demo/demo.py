from backend.engine.tos.abilities.doctor import DoctorAbility
from backend.engine.tos.abilities.jailor import JailorDayAbility, JailorExecuteAbility
from backend.engine.tos.abilities.mafioso import MafiosoAbility
from backend.engine.tos.abilities.sheriff import SheriffAbility
from backend.engine.tos.core.resolver import Resolver
from backend.engine.tos.enums.phase import Phase
from backend.engine.tos.models.events import GameState
from backend.engine.tos.models.player import Player
from backend.engine.tos.registry.role_registry import ROLE_REGISTRY


def main():
    resolver = Resolver(ROLE_REGISTRY)

    players = {
        1: {"name": "Mafioso", "role": ROLE_REGISTRY["mafioso"]},
        2: {"name": "Sheriff", "role": ROLE_REGISTRY["sheriff"]},
        3: {"name": "Doctor", "role": ROLE_REGISTRY["doctor"]},
        4: {"name": "Jailor", "role": ROLE_REGISTRY["jailor"]},
    }

    state = GameState(
        phase=Phase.DAY,
        players={pid: Player(
            pid=pid,
            name=data["name"],
            role=data["role"],
        ) for pid, data in players.items()}
    )

    state.queue_intent(JailorDayAbility().create_intent(state, actor=4, target=3))

    events = resolver.resolve_day(state)

    print("Day Events")
    for e in events:
        print(f"{e.type.name}: actor={e.actor}, target={e.target}, messages={e.messages!r}")

    print("Player Status")
    for pid, p in state.players.items():
        print(f"{pid} ({p.name} - {p.role.key}): {p.status!r}")
    state.clear_queue()
    state.phase = Phase.NIGHT

    state.queue_intent(SheriffAbility().create_intent(state, actor=2, target=1))

    state.queue_intent(MafiosoAbility().create_intent(state, actor=1, target=2))

    state.queue_intent(DoctorAbility().create_intent(state, actor=3, target=2))

    state.queue_intent(JailorExecuteAbility().create_intent(state, actor=4, target=3))

    events = resolver.resolve_night(state)

    print("Night Events")
    for e in events:
        print(f"{e.type.name}: actor={e.actor}, target={e.target}, messages={e.messages!r}")

    print("Alive")
    for pid, p in state.players.items():
        print(f"{pid} ({p.name} - {p.role.key}): {'ALIVE' if p.alive else 'DEAD'}")


if __name__ == "__main__":
    main()
