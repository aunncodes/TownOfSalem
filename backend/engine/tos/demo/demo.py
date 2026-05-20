from backend.engine.tos.manager.game_manager import GameManager
from backend.engine.tos.registry.role_registry import ROLE_REGISTRY


def ask_int(message):
    while True:
        raw = input(message)

        try:
            return int(raw)
        except ValueError:
            print("Enter a number.")


def choose(title, values):
    print(title)

    for index, value in enumerate(values, start=1):
        print(f"{index}: {value}")

    while True:
        choice = ask_int("> ")

        if 1 <= choice <= len(values):
            return choice - 1

        print("Invalid choice.")


def choose_role():
    role_items = list(ROLE_REGISTRY.items())
    roles = [role.name for _, role in role_items]

    role = choose("Choose role:", roles)

    return role_items[role][0]


def create_players():
    player_count = ask_int("How many players? ")

    players = {}

    for pid in range(1, player_count + 1):
        name = input(f"Name for Player {pid}: ")
        role_key = choose_role()

        players[pid] = {
            "name": name,
            "role": role_key,
        }

    return players

def print_players(manager):
    state = manager.require_state()

    print("Players")

    for pid, player in state.players.items():
        alive = "ALIVE" if player.alive else "DEAD"
        print(f"{pid}. {player.name} - {player.role.name} - {alive}")


def print_events(events):
    print("Events")

    if len(events) == 0:
        print("No events.")
        return

    for event in events:
        print(
            f"{event.type.name}: "
            f"actor={event.actor}, "
            f"target={event.target}, "
            f"messages={event.messages!r}"
        )


def choose_target(manager, actor):
    targets = manager.get_valid_targets(actor)

    if len(targets) == 0:
        return None

    target_items = list(targets.items())
    target_names = [player.name for _, player in target_items]

    target = choose("Choose target:", target_names)

    return target_items[target][0]


def choose_action(manager, actor):
    state = manager.require_state()
    player = state.require_player(actor)

    choices = manager.get_action_choices(actor)

    if len(choices) == 0:
        return

    print(f"{player.name}'s action")
    print(f"Role: {player.role.name}")
    print(f"Phase: {state.phase.name}")

    action_names = ["nothing"] + [choice.name for choice in choices]

    action = choose("Choose action:", action_names)

    if action == 0:
        return

    action = choices[action - 1]

    target = None

    if action.requires_target:
        target = choose_target(manager, actor)

    try:
        manager.submit_action(
            actor=actor,
            ability_key=action.name,
            target=target,
        )
    except ValueError as error:
        print(f"Invalid action: {error}")


def play_phase(manager):
    state = manager.require_state()

    print(f"Current phase: {state.phase.name}")

    for actor in state.players:
        player = state.players[actor]

        if not player.alive:
            continue

        choose_action(manager, actor)

    events = manager.resolve_phase()
    print_events(events)

    manager.advance_phase()


def main():
    manager = GameManager()

    players = create_players()
    manager.create_game(players)

    while not manager.is_game_over():
        print_players(manager)
        play_phase(manager)

    print_players(manager)

    winner = manager.get_winner()

    print("Game over.")

    if winner is None:
        print("No winner.")
    else:
        print(f"Winner: {winner.name}")


if __name__ == "__main__":
    main()