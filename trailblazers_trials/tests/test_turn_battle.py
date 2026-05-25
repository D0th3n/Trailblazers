from pathlib import Path
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = PROJECT_ROOT / "game"
CHAPTER_TWO_FILE = GAME_ROOT / "chapters" / "chapter_02.rpy"
IMAGES_FILE = GAME_ROOT / "images.rpy"
SCENE_OBJECTIVE_DATA_FILE = GAME_ROOT / "scene_objectives_data.py"
TURN_BATTLE_SYSTEM_FILE = GAME_ROOT / "systems" / "turn_battle.rpy"
VARIABLES_FILE = GAME_ROOT / "variables.rpy"
if str(GAME_ROOT) not in sys.path:
    sys.path.insert(0, str(GAME_ROOT))


import combat_data
import combat_model


class TurnBattleModelTests(unittest.TestCase):

    def test_battle_starts_with_player_turn_and_full_hp(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])

        self.assertEqual(state["turn"], "player")
        self.assertEqual(state["player"]["hp"], state["player"]["max_hp"])
        self.assertEqual(state["player"]["ap"], state["player"]["max_ap"])
        self.assertEqual(state["enemy"]["ap"], state["enemy"]["max_ap"])
        self.assertEqual(state["enemy"]["hp"], state["enemy"]["max_hp"])
        self.assertIsNone(state["outcome"])

    def test_battle_state_uses_party_structure_with_active_actor(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])

        self.assertIn("party", state)
        self.assertEqual(len(state["party"]), 1)
        self.assertEqual(state["active_actor_id"], "oren")
        self.assertIs(state["player"], state["party"][0])
        self.assertIs(combat_model.active_actor(state), state["party"][0])
        self.assertEqual(state["party"][0]["slot_index"], 0)

    def test_legacy_single_player_encounters_are_normalized_to_party(self):
        encounter = {
            "title": "Legacy",
            "summary": "Single player fallback.",
            "player": combat_data.BATTLE_ENCOUNTERS["meditation_dummy"]["party"][0],
            "enemy": combat_data.BATTLE_ENCOUNTERS["meditation_dummy"]["enemy"],
            "actions": combat_data.BATTLE_ENCOUNTERS["meditation_dummy"]["actions"],
        }

        state = combat_model.start_battle(encounter)

        self.assertEqual(len(state["party"]), 1)
        self.assertEqual(state["active_actor_id"], "oren")
        self.assertIs(state["player"], state["party"][0])

    def test_attack_damages_enemy_and_enemy_counterattacks(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])

        updated = combat_model.resolve_player_action(state, "attack")

        self.assertEqual(updated["enemy"]["hp"], 14)
        self.assertEqual(updated["player"]["hp"], 26)
        self.assertEqual(updated["player"]["ap"], 4)
        self.assertEqual(updated["enemy"]["ap"], 4)
        self.assertIn("Oren strikes the training shade", updated["log"][-2])
        self.assertIn("The training shade answers", updated["log"][-1])

    def test_guard_reduces_enemy_counterattack(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])

        updated = combat_model.resolve_player_action(state, "guard")

        self.assertEqual(updated["player"]["hp"], 28)
        self.assertEqual(updated["enemy"]["hp"], 20)
        self.assertFalse(updated["player"]["guarding"])

    def test_ember_focus_deals_heavier_damage(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])

        updated = combat_model.resolve_player_action(state, "ember_focus")

        self.assertEqual(updated["enemy"]["hp"], 10)
        self.assertEqual(updated["player"]["hp"], 26)
        self.assertEqual(updated["player"]["ap"], 3)

    def test_action_cannot_fire_without_enough_ap(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])
        state["player"]["ap"] = 0

        updated = combat_model.resolve_player_action(state, "attack")

        self.assertEqual(updated["enemy"]["hp"], 20)
        self.assertEqual(updated["player"]["hp"], 30)
        self.assertIn("not enough AP", updated["log"][-1])

    def test_invalid_action_logs_warning_without_changing_state(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])

        updated = combat_model.resolve_player_action(state, "unknown_action")

        self.assertEqual(updated["enemy"]["hp"], 20)
        self.assertEqual(updated["player"]["hp"], 30)
        self.assertEqual(updated["player"]["ap"], 5)
        self.assertIn("cannot use that action", updated["log"][-1])

    def test_focus_restores_ap_without_exceeding_maximum(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])
        state["player"]["ap"] = 1

        updated = combat_model.resolve_player_action(state, "focus")

        self.assertEqual(updated["player"]["ap"], 4)
        self.assertEqual(updated["player"]["max_ap"], 5)
        self.assertEqual(updated["enemy"]["hp"], 20)
        self.assertEqual(updated["player"]["hp"], 26)

    def test_focus_caps_ap_at_actor_maximum(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])
        state["player"]["ap"] = 4

        updated = combat_model.resolve_player_action(state, "focus")

        self.assertEqual(updated["player"]["ap"], 5)

    def test_enemy_recovers_ap_when_it_cannot_counterattack(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])
        state["enemy"]["ap"] = 0

        updated = combat_model.resolve_player_action(state, "attack")

        self.assertEqual(updated["enemy"]["hp"], 14)
        self.assertEqual(updated["player"]["hp"], 30)
        self.assertEqual(updated["enemy"]["ap"], 2)
        self.assertIn("gathers its rhythm", updated["log"][-1])

    def test_victory_stops_enemy_counterattack(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])
        state["enemy"]["hp"] = 4

        updated = combat_model.resolve_player_action(state, "attack")

        self.assertEqual(updated["enemy"]["hp"], 0)
        self.assertEqual(updated["player"]["hp"], 30)
        self.assertEqual(updated["outcome"], "victory")

    def test_defeat_is_recorded_after_enemy_counterattack(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])
        state["player"]["hp"] = 2

        updated = combat_model.resolve_player_action(state, "guard")

        self.assertEqual(updated["player"]["hp"], 0)
        self.assertEqual(updated["outcome"], "defeat")


class TurnBattleRenpyIntegrationTests(unittest.TestCase):

    def test_chapter_two_room_has_meditation_hotspot(self):
        data_text = SCENE_OBJECTIVE_DATA_FILE.read_text()

        self.assertIn('"meditation"', data_text)
        self.assertIn('"label": "Meditation"', data_text)
        self.assertIn('"description": "Train inside Oren', data_text)

    def test_chapter_two_routes_meditation_to_training_battle(self):
        chapter_text = CHAPTER_TWO_FILE.read_text()

        self.assertIn('if chapter_02_room_choice == "meditation":', chapter_text)
        self.assertIn("call chapter_02_meditation_training", chapter_text)
        self.assertIn("label chapter_02_meditation_training:", chapter_text)
        self.assertIn('call turn_battle("meditation_dummy")', chapter_text)

    def test_turn_battle_runtime_exists(self):
        system_text = TURN_BATTLE_SYSTEM_FILE.read_text()
        variables_text = VARIABLES_FILE.read_text()

        self.assertIn("default turn_battle_state = None", variables_text)
        self.assertIn("default turn_battle_encounter_id = None", variables_text)
        self.assertIn("import combat_model", system_text)
        self.assertIn("import combat_data", system_text)
        self.assertIn("label turn_battle(encounter_id):", system_text)
        self.assertIn("$ turn_battle_encounter_id = encounter_id", system_text)
        self.assertIn("screen turn_battle_screen():", system_text)
        self.assertIn("action Return(action_id)", system_text)
        self.assertIn("turn_battle_resolve_player_action", system_text)
        self.assertIn('if turn_battle_choice == "retry":', system_text)
        self.assertIn("turn_battle_start(turn_battle_encounter_id)", system_text)
        self.assertIn("jump turn_battle_loop", system_text)

    def test_turn_battle_uses_side_view_jrpg_layout(self):
        system_text = TURN_BATTLE_SYSTEM_FILE.read_text()

        self.assertIn("turn_battle_background()", system_text)
        self.assertIn("turn_battle_party()", system_text)
        self.assertIn("turn_battle_active_actor()", system_text)
        self.assertIn("turn_battle_player_sprite", system_text)
        self.assertIn("turn_battle_party_sprite", system_text)
        self.assertIn("screen turn_battle_party_status", system_text)
        self.assertIn("turn_battle_enemy_sprite", system_text)
        self.assertIn("screen turn_battle_ap_meter", system_text)
        self.assertIn("screen turn_battle_action_row", system_text)
        self.assertIn("turn_battle_action_enabled", system_text)
        self.assertIn("turn_battle_player_ap_text()", system_text)
        self.assertIn("turn_battle_enemy_ap_text()", system_text)
        self.assertIn('style "turn_battle_command_panel"', system_text)
        self.assertIn('style "turn_battle_status_panel"', system_text)
        self.assertIn('style "turn_battle_message_panel"', system_text)
        self.assertIn("Action Menu", system_text)
        self.assertIn("Stock", system_text)
        self.assertIn("Offense", system_text)
        self.assertIn("Use Consumable Items", system_text)
        self.assertIn('action_id="focus"', system_text)
        self.assertIn('cost_text="+3 AP"', system_text)
        self.assertIn('key "K_a" action Return("attack")', system_text)
        self.assertIn('key "K_f" action Return("ember_focus")', system_text)
        self.assertIn('key "K_s" action Return("focus")', system_text)
        self.assertIn('key "K_d" action Return("guard")', system_text)
        self.assertIn("Retry", system_text)
        self.assertIn("Exit Training", system_text)
        self.assertIn("HP [party_actor['hp']] / [party_actor['max_hp']]", system_text)
        self.assertIn("MP --", system_text)
        self.assertIn("STA --", system_text)
        self.assertIn("CHAOS --", system_text)

    def test_player_sprite_has_clickable_quick_actions(self):
        system_text = TURN_BATTLE_SYSTEM_FILE.read_text()

        self.assertIn("use turn_battle_player_action_hotspot(player, outcome)", system_text)
        self.assertIn("screen turn_battle_player_action_hotspot(player, outcome):", system_text)
        self.assertIn('action ToggleScreen("turn_battle_player_quick_actions")', system_text)
        self.assertIn("screen turn_battle_player_quick_actions():", system_text)
        self.assertIn("xalign 0.78", system_text)
        self.assertIn("yalign 0.64", system_text)
        self.assertIn("zoom 0.92", system_text)
        self.assertIn('[Hide("turn_battle_player_quick_actions"), Return("attack")]', system_text)
        self.assertIn('[Hide("turn_battle_player_quick_actions"), Return("ember_focus")]', system_text)
        self.assertIn('[Hide("turn_battle_player_quick_actions"), Return("focus")]', system_text)
        self.assertIn('[Hide("turn_battle_player_quick_actions"), Return("guard")]', system_text)
        self.assertIn("xpos 1160", system_text)
        self.assertIn("ypos 310", system_text)
        self.assertIn("xsize 220", system_text)
        self.assertIn("ysize 310", system_text)

    def test_training_encounter_defines_placeholder_sprites(self):
        encounter = combat_data.BATTLE_ENCOUNTERS["meditation_dummy"]

        self.assertEqual(encounter["background"], "bg severance dark")
        self.assertEqual(encounter["party"][0]["id"], "oren")
        self.assertEqual(encounter["party"][0]["max_ap"], 5)
        self.assertEqual(encounter["enemy"]["max_ap"], 5)
        self.assertEqual(encounter["enemy"]["attack_cost"], 1)
        self.assertEqual(encounter["actions"]["attack"]["cost"], 1)
        self.assertEqual(encounter["actions"]["focus"]["restores_ap"], 3)
        self.assertEqual(encounter["party"][0]["sprite"], "combat oren temp idle")
        self.assertEqual(encounter["enemy"]["sprite"], "combat training dummy temp idle")

    def test_temp_combat_sprite_assets_are_registered(self):
        images_text = IMAGES_FILE.read_text()

        self.assertIn(
            'image combat oren temp idle = "images/combat/oren_temp_idle.png"',
            images_text,
        )
        self.assertIn(
            'image combat training dummy temp idle = "images/combat/training_dummy_temp_idle.png"',
            images_text,
        )
        self.assertTrue((GAME_ROOT / "images" / "combat" / "oren_temp_idle.png").exists())
        self.assertTrue((GAME_ROOT / "images" / "combat" / "training_dummy_temp_idle.png").exists())


if __name__ == "__main__":
    unittest.main()
