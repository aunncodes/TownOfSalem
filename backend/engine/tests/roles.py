import unittest
from backend.engine.tos.enums.game_event import GameEventType
from backend.engine.tos.enums.phase import Phase
from backend.engine.tos.enums.status import StatusType
from backend.engine.tos.manager.game_manager import GameManager


class RoleMechanicsTest(unittest.TestCase):
    def make_game(self, players):
        manager = GameManager()
        manager.create_game({
            pid: {"name": name, "role": role}
            for pid, name, role in players
        })
        return manager

    def start_night(self, manager):
        self.assertEqual(manager.require_state().phase, Phase.DAY)
        manager.advance_phase()
        self.assertEqual(manager.require_state().phase, Phase.NIGHT)

    def event_types(self, events):
        return [event.type for event in events]

    def find_event(self, events, event_type, actor=None):
        for event in events:
            if event.type != event_type:
                continue
            if actor is not None and event.actor != actor:
                continue
            return event
        self.fail("Missing event: " + event_type.name)

    def test_mafioso_kills_target(self):
        manager = self.make_game([
            (1, "Mafioso", "mafioso"),
            (2, "Sheriff", "sheriff"),
        ])
        self.start_night(manager)

        manager.submit_action(1, "attack", 2)
        events = manager.resolve_phase()

        self.assertIn(GameEventType.KILL, self.event_types(events))
        self.assertFalse(manager.require_state().require_player(2).alive)

    def test_doctor_protects_target_from_mafioso(self):
        manager = self.make_game([
            (1, "Mafioso", "mafioso"),
            (2, "Doctor", "doctor"),
            (3, "Sheriff", "sheriff"),
        ])
        self.start_night(manager)

        manager.submit_action(2, "protect", 3)
        manager.submit_action(1, "attack", 3)
        events = manager.resolve_phase()

        self.assertIn(GameEventType.TARGET_PROTECTED, self.event_types(events))
        self.assertIn(GameEventType.ATTACK_BLOCKED, self.event_types(events))
        self.assertTrue(manager.require_state().require_player(3).alive)

    def test_tavern_keeper_roleblocks_mafioso(self):
        manager = self.make_game([
            (1, "Tavern Keeper", "tavernkeeper"),
            (2, "Mafioso", "mafioso"),
            (3, "Sheriff", "sheriff"),
        ])
        self.start_night(manager)

        manager.submit_action(1, "roleblock", 2)
        manager.submit_action(2, "attack", 3)
        events = manager.resolve_phase()

        state = manager.require_state()
        self.assertIn(GameEventType.TARGET_ROLEBLOCKED, self.event_types(events))
        self.assertNotIn(GameEventType.KILL, self.event_types(events))
        self.assertTrue(state.require_player(3).alive)
        self.assertTrue(state.require_player(2).has_status(StatusType.ROLEBLOCKED))

        manager.advance_phase()
        self.assertFalse(state.require_player(2).has_status(StatusType.ROLEBLOCKED))

    def test_sheriff_finds_mafioso_suspicious(self):
        manager = self.make_game([
            (1, "Sheriff", "sheriff"),
            (2, "Mafioso", "mafioso"),
        ])
        self.start_night(manager)

        manager.submit_action(1, "sheriff", 2)
        events = manager.resolve_phase()

        event = self.find_event(events, GameEventType.SHERIFF_RESULT, actor=1)
        self.assertIn("suspicious", event.messages[1])

    def test_investigator_gets_role_result(self):
        manager = self.make_game([
            (1, "Investigator", "investigator"),
            (2, "Doctor", "doctor"),
        ])
        self.start_night(manager)

        manager.submit_action(1, "investigator", 2)
        events = manager.resolve_phase()

        state = manager.require_state()
        event = self.find_event(events, GameEventType.INVESTIGATION_RESULT, actor=1)
        self.assertEqual(event.messages[1], state.require_player(2).role.data.investigator_result)

    def test_jailor_selects_and_executes_jailed_target(self):
        manager = self.make_game([
            (1, "Jailor", "jailor"),
            (2, "Mafioso", "mafioso"),
        ])

        manager.submit_action(1, "jailorselect", 2)
        day_events = manager.resolve_phase()
        state = manager.require_state()

        self.assertIn(GameEventType.JAIL_SELECTED, self.event_types(day_events))
        self.assertTrue(state.require_player(2).has_status(StatusType.JAILED))

        manager.advance_phase()
        manager.submit_action(1, "execute", 2)
        night_events = manager.resolve_phase()

        self.assertIn(GameEventType.KILL, self.event_types(night_events))
        self.assertFalse(state.require_player(2).alive)

    def test_veteran_alert_shoots_visitor(self):
        manager = self.make_game([
            (1, "Veteran", "veteran"),
            (2, "Mafioso", "mafioso"),
        ])
        self.start_night(manager)

        manager.submit_action(1, "alert")
        manager.submit_action(2, "attack", 1)
        events = manager.resolve_phase()

        state = manager.require_state()
        self.assertIn(GameEventType.VETERAN_ALERTED, self.event_types(events))
        self.assertIn(GameEventType.VETERAN_SHOT, self.event_types(events))
        self.assertTrue(state.require_player(1).alive)
        self.assertFalse(state.require_player(2).alive)

        manager.advance_phase()
        self.assertFalse(state.require_player(1).has_status(StatusType.ALERT))

    def test_lookout_sees_visitor(self):
        manager = self.make_game([
            (1, "Lookout", "lookout"),
            (2, "Mafioso", "mafioso"),
            (3, "Doctor", "doctor"),
        ])
        self.start_night(manager)

        manager.submit_action(1, "lookout", 3)
        manager.submit_action(2, "attack", 3)
        events = manager.resolve_phase()

        event = self.find_event(events, GameEventType.LOOKOUT_SAW, actor=1)
        self.assertEqual(event.target, 3)
        self.assertIn("Mafioso", event.messages[1])

    def test_framer_frame_affects_multiple_checks_before_expiring(self):
        manager = self.make_game([
            (1, "Framer", "framer"),
            (2, "Sheriff", "sheriff"),
            (3, "Investigator", "investigator"),
            (4, "Doctor", "doctor"),
        ])
        self.start_night(manager)

        manager.submit_action(1, "frame", 4)
        manager.submit_action(2, "sheriff", 4)
        manager.submit_action(3, "investigator", 4)
        events = manager.resolve_phase()

        state = manager.require_state()
        sheriff_event = self.find_event(events, GameEventType.SHERIFF_RESULT, actor=2)
        investigator_event = self.find_event(events, GameEventType.INVESTIGATION_RESULT, actor=3)
        framed_status = state.require_player(4).get_statuses(StatusType.FRAMED)[0]

        self.assertIn("suspicious", sheriff_event.messages[2])
        self.assertNotEqual(investigator_event.messages[3], state.require_player(4).role.data.investigator_result) # Just check if the result is different to imply the framer changed the results
        self.assertTrue(framed_status.data["checked"])
        self.assertTrue(state.require_player(4).has_status(StatusType.FRAMED))

        manager.advance_phase()
        self.assertFalse(state.require_player(4).has_status(StatusType.FRAMED))


if __name__ == "__main__":
    unittest.main()
