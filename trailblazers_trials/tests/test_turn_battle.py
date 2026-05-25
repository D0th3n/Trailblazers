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
        self.assertEqual(state["player"]["qana"], state["player"]["max_qana"])
        self.assertEqual(state["player"]["stamina"], state["player"]["max_stamina"])
        self.assertEqual(state["player"]["chaos"], 0)
        self.assertEqual(state["enemy"]["ap"], state["enemy"]["max_ap"])
        self.assertEqual(state["enemy"]["hp"], state["enemy"]["max_hp"])
        self.assertEqual(state["round"], 1)
        self.assertEqual(state["round_action_uses"], {})
        self.assertIn("Battle Start", state["log"])
        self.assertIn("Click Oren to choose an action.", state["log"])
        self.assertIsNone(state["outcome"])

    def test_battle_state_uses_party_structure_with_active_actor(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])

        self.assertIn("party", state)
        self.assertIn("enemies", state)
        self.assertEqual(len(state["party"]), 1)
        self.assertEqual(len(state["enemies"]), 1)
        self.assertEqual(state["active_actor_id"], "oren")
        self.assertIs(state["player"], state["party"][0])
        self.assertIs(state["enemy"], state["enemies"][0])
        self.assertIs(combat_model.active_actor(state), state["party"][0])
        self.assertEqual(state["party"][0]["slot_index"], 0)

    def test_team_battle_adds_ally_and_second_enemy_to_turn_order(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["team_dummy"])

        self.assertEqual([actor["id"] for actor in state["party"]], ["oren", "ally_dummy"])
        self.assertEqual(
            [actor["id"] for actor in state["enemies"]],
            ["training_shade", "support_shade"],
        )
        self.assertEqual(
            [entry["id"] for entry in state["turn_order"]],
            ["oren", "ally_dummy", "training_shade", "support_shade"],
        )
        self.assertEqual(state["active_actor_id"], "oren")

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
        self.assertEqual(updated["player"]["ap"], 3)
        self.assertEqual(updated["enemy"]["ap"], 2)
        self.assertEqual(updated["enemy"]["qana"], 4)
        self.assertIn("Oren strikes the training shade", updated["log"][-2])
        self.assertIn("Training Shade casts Freeze Ray", updated["log"][-1])

    def test_team_battle_player_controls_ally_before_enemies_answer(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["team_dummy"])

        ally_turn = combat_model.resolve_player_action(state, "attack")

        self.assertEqual(ally_turn["enemies"][0]["hp"], 14)
        self.assertEqual(ally_turn["player"]["id"], "ally_dummy")
        self.assertEqual(ally_turn["active_actor_id"], "ally_dummy")
        self.assertEqual(ally_turn["player"]["hp"], 28)
        self.assertEqual(combat_model.action_uses_remaining(ally_turn, "attack"), 5)
        self.assertIn("Ally Dummy is ready to act.", ally_turn["log"][-1])

        next_round = combat_model.resolve_player_action(ally_turn, "attack")

        self.assertEqual(next_round["enemies"][0]["hp"], 8)
        self.assertEqual(next_round["party"][1]["hp"], 22)
        self.assertEqual(next_round["party"][1]["ap"], 3)
        self.assertEqual(next_round["active_actor_id"], "ally_dummy")
        self.assertEqual(next_round["round"], 1)
        self.assertTrue(next_round["pending_round_start"])
        self.assertIn("Enemy Support Dummy answers", " ".join(next_round["log"]))

        advanced = combat_model.begin_pending_round(next_round)
        self.assertEqual(advanced["active_actor_id"], "oren")
        self.assertEqual(advanced["round"], 2)
        self.assertEqual(advanced["party"][0]["ap"], 5)
        self.assertEqual(advanced["party"][1]["ap"], 5)

    def test_dragon_spells_are_locked_to_allowed_actors(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["team_dummy"])

        ally_turn = combat_model.resolve_player_action(state, "attack")
        blocked = combat_model.resolve_player_action(ally_turn, "dragon_geisure")

        self.assertEqual(blocked["enemies"][0]["hp"], 14)
        self.assertEqual(blocked["active_actor_id"], "ally_dummy")
        self.assertFalse(combat_model.action_can_be_used(blocked, "dragon_geisure"))
        self.assertIn("cannot use Dragon Spells", blocked["log"][-1])

    def test_spell_tiers_change_effective_action_values(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])

        tier_one = combat_model.action_for_actor(state, state["player"], "fire_ball")
        self.assertEqual(tier_one["label"], "Fire Ball I")
        self.assertEqual(tier_one["damage"], 4)
        self.assertEqual(tier_one["qana_cost"], 3)

        combat_model.set_actor_skill_tier(state, "oren", "fire_ball", 2)
        tier_two = combat_model.action_for_actor(state, state["player"], "fire_ball")

        self.assertEqual(tier_two["label"], "Fire Ball II")
        self.assertEqual(tier_two["damage"], 6)
        self.assertEqual(tier_two["qana_cost"], 4)

    def test_guard_reduces_enemy_counterattack(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])

        updated = combat_model.resolve_player_action(state, "guard")

        self.assertEqual(updated["player"]["hp"], 28)
        self.assertEqual(updated["enemy"]["hp"], 20)
        self.assertEqual(updated["player"]["ap"], 5)
        self.assertEqual(updated["player"]["stamina"], 4)
        self.assertFalse(updated["player"]["guarding"])

    def test_defense_requires_stamina(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])
        state["player"]["stamina"] = 1

        updated = combat_model.resolve_player_action(state, "guard")

        self.assertEqual(updated["player"]["hp"], 30)
        self.assertIn("not enough Stamina", updated["log"][-1])
        self.assertFalse(combat_model.action_can_be_used(updated, "guard"))

    def test_dodge_can_avoid_the_next_attack_and_heal(self):
        original_random = combat_model.random.random
        combat_model.random.random = lambda: 0.1
        try:
            state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])
            state["player"]["hp"] = 20

            updated = combat_model.resolve_player_action(state, "dodge")
        finally:
            combat_model.random.random = original_random

        self.assertEqual(updated["player"]["hp"], 21)
        self.assertEqual(updated["player"]["stamina"], 4)
        self.assertFalse(updated["player"]["dodging"])
        self.assertIn("dodges Training Shade's Freeze Ray", updated["log"][-1])

    def test_failed_dodge_takes_the_next_attack(self):
        original_random = combat_model.random.random
        combat_model.random.random = lambda: 0.9
        try:
            state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])
            state["player"]["hp"] = 20

            updated = combat_model.resolve_player_action(state, "dodge")
        finally:
            combat_model.random.random = original_random

        self.assertEqual(updated["player"]["hp"], 16)
        self.assertFalse(updated["player"]["dodging"])
        self.assertIn("fails to dodge", " ".join(updated["log"]))

    def test_ember_focus_deals_heavier_damage(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])

        updated = combat_model.resolve_player_action(state, "ember_focus")

        self.assertEqual(updated["enemy"]["hp"], 10)
        self.assertEqual(updated["player"]["hp"], 26)
        self.assertEqual(updated["player"]["ap"], 0)
        self.assertEqual(updated["round"], 1)
        self.assertTrue(updated["pending_round_start"])

        advanced = combat_model.begin_pending_round(updated)
        self.assertEqual(advanced["player"]["ap"], 5)
        self.assertEqual(advanced["round"], 2)

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

    def test_qana_spell_spends_qana_and_ap_for_initial_and_tick_damage(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])
        state["enemy"]["hp"] = 999

        updated = combat_model.resolve_player_action(state, "fire_ball")

        self.assertEqual(updated["enemy"]["hp"], 995)
        self.assertEqual(updated["player"]["ap"], 3)
        self.assertEqual(updated["player"]["qana"], 7)
        self.assertEqual(updated["enemy"]["status_effects"][0]["damage"], 2)
        self.assertEqual(updated["enemy"]["status_effects"][0]["rounds"], 3)

        updated["player"]["ap"] = 0
        updated = combat_model.resolve_player_action(updated, "guard")

        self.assertEqual(updated["round"], 1)
        self.assertEqual(updated["player"]["ap"], 0)
        self.assertTrue(updated["pending_round_start"])

        updated = combat_model.begin_pending_round(updated)
        self.assertEqual(updated["round"], 2)
        self.assertEqual(updated["enemy"]["hp"], 993)
        self.assertIn("lingering fire damage", " ".join(updated["log"]))

    def test_dragon_spells_build_chaos_and_max_chaos_causes_defeat(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])
        state["enemy"]["hp"] = 999
        state["player"]["chaos"] = 5

        updated = combat_model.resolve_player_action(state, "dragon_geisure")

        self.assertEqual(updated["player"]["chaos"], 10)
        self.assertEqual(updated["player"]["hp"], 0)
        self.assertEqual(updated["outcome"], "defeat")
        self.assertIn("Jotunn seizes control", updated["log"][-1])

    def test_healing_burst_restores_hp_and_spends_qana(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])
        state["player"]["hp"] = 10

        updated = combat_model.resolve_player_action(state, "healing_burst")

        self.assertEqual(updated["player"]["hp"], 11)
        self.assertEqual(updated["player"]["qana"], 7)
        self.assertEqual(updated["player"]["ap"], 3)

    def test_freeze_ray_stops_enemy_counterattacks_for_two_rounds(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])

        frozen = combat_model.resolve_player_action(state, "freeze_ray")
        self.assertEqual(frozen["player"]["hp"], 30)
        self.assertEqual(frozen["enemy"]["skip_counterattacks"], 1)
        self.assertIn("frozen", frozen["log"][-1])

        followup = combat_model.resolve_player_action(frozen, "attack")
        self.assertEqual(followup["player"]["hp"], 30)
        self.assertEqual(followup["enemy"]["skip_counterattacks"], 0)

    def test_items_have_one_of_two_uses_and_restore_resources(self):
        state = combat_model.start_battle(
            combat_data.BATTLE_ENCOUNTERS["meditation_dummy"],
            inventory={
                "health_elixir": 1,
                "qana_elixir": 1,
            },
        )
        state["player"]["hp"] = 10
        state["player"]["qana"] = 4

        self.assertEqual(combat_model.action_uses_remaining(state, "health_elixir"), 1)
        self.assertEqual(combat_model.action_use_capacity(state, "health_elixir"), 2)

        healed = combat_model.resolve_player_action(state, "health_elixir")
        restored = combat_model.resolve_player_action(healed, "qana_elixir")

        self.assertEqual(restored["player"]["hp"], 5)
        self.assertEqual(restored["player"]["qana"], 7)
        self.assertEqual(combat_model.action_uses_remaining(restored, "health_elixir"), 0)
        self.assertEqual(combat_model.action_uses_remaining(restored, "qana_elixir"), 0)
        self.assertFalse(combat_model.action_can_be_used(restored, "health_elixir"))

    def test_limited_actions_track_remaining_uses_per_round(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])

        self.assertEqual(combat_model.action_uses_remaining(state, "attack"), 5)
        self.assertEqual(combat_model.action_uses_remaining(state, "focus"), 1)
        self.assertIsNone(combat_model.action_uses_remaining(state, "guard"))

        updated = combat_model.resolve_player_action(state, "attack")

        self.assertEqual(combat_model.action_uses_remaining(updated, "attack"), 4)
        self.assertTrue(combat_model.action_can_be_used(updated, "attack"))

    def test_support_can_only_be_used_once_per_round(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])
        state["player"]["ap"] = 1

        updated = combat_model.resolve_player_action(state, "focus")
        blocked = combat_model.resolve_player_action(updated, "focus")

        self.assertEqual(blocked["player"]["ap"], 4)
        self.assertEqual(blocked["player"]["hp"], 26)
        self.assertEqual(combat_model.action_uses_remaining(blocked, "focus"), 0)
        self.assertFalse(combat_model.action_can_be_used(blocked, "focus"))
        self.assertIn("already used", blocked["log"][-1])

    def test_round_resets_ap_and_limited_actions_when_ap_is_spent(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])
        state["enemy"]["hp"] = 999

        state = combat_model.resolve_player_action(state, "ember_focus")

        self.assertEqual(state["round"], 1)
        self.assertEqual(state["player"]["ap"], 0)
        self.assertTrue(state["pending_round_start"])

        state = combat_model.begin_pending_round(state)
        self.assertEqual(state["round"], 2)
        self.assertEqual(state["player"]["ap"], 5)
        self.assertEqual(state["enemy"]["ap"], 5)
        self.assertEqual(combat_model.action_uses_remaining(state, "attack"), 5)
        self.assertIn("Round 2 begins.", state["log"][-1])

    def test_defense_can_be_used_without_ap(self):
        state = combat_model.start_battle(combat_data.BATTLE_ENCOUNTERS["meditation_dummy"])
        state["player"]["ap"] = 0

        updated = combat_model.resolve_player_action(state, "guard")

        self.assertEqual(updated["player"]["hp"], 28)
        self.assertEqual(updated["player"]["ap"], 0)
        self.assertEqual(updated["player"]["stamina"], 4)
        self.assertEqual(updated["round"], 1)
        self.assertTrue(updated["pending_round_start"])

        updated = combat_model.begin_pending_round(updated)
        self.assertEqual(updated["player"]["ap"], 5)
        self.assertEqual(updated["player"]["stamina"], 6)
        self.assertEqual(updated["round"], 2)

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
        self.assertIn('if party_actor["sprite"] == "combat oren idle":', system_text)
        self.assertIn("screen turn_battle_party_status", system_text)
        self.assertIn("turn_battle_enemy_sprite", system_text)
        self.assertIn("screen turn_battle_ap_meter", system_text)
        self.assertIn("screen turn_battle_action_row", system_text)
        self.assertIn("turn_battle_action_enabled", system_text)
        self.assertIn("turn_battle_player_ap_text()", system_text)
        self.assertIn("turn_battle_actor_ap_text(party_actor)", system_text)
        self.assertIn("turn_battle_party_actor_name(party_actor)", system_text)
        self.assertIn("turn_battle_enemy_ap_text()", system_text)
        self.assertIn('style "turn_battle_command_panel"', system_text)
        self.assertIn('style "turn_battle_status_panel"', system_text)
        self.assertIn('style "turn_battle_message_panel"', system_text)
        self.assertIn("Battle Start", system_text)
        self.assertIn('return "Click %s to choose an action." % actor["name"]', system_text)
        self.assertIn("turn_battle_action_uses_text", system_text)
        self.assertIn("uses_text=turn_battle_action_uses_text", system_text)
        self.assertIn("turn_battle_action_label", system_text)
        self.assertIn('style "turn_battle_prompt_panel"', system_text)
        self.assertIn("Stock", system_text)
        self.assertIn("Training Dummy", system_text)
        self.assertIn("screen turn_battle_enemy_status", system_text)
        self.assertIn('text "VS":', system_text)
        self.assertIn("Use Consumable Items", system_text)
        self.assertIn("QANA %d / %d", system_text)
        self.assertIn('action_id="focus"', system_text)
        self.assertIn('cost_text=turn_battle_action_cost_text("focus")', system_text)
        self.assertNotIn('key "K_a" action Return("attack")', system_text)
        self.assertNotIn('key "K_f" action Return("ember_focus")', system_text)
        self.assertNotIn('key "K_s" action Return("focus")', system_text)
        self.assertNotIn('key "K_d" action Return("guard")', system_text)
        self.assertIn("Retry", system_text)
        self.assertIn("Exit Training", system_text)
        self.assertIn("HP [party_actor['hp']] / [party_actor['max_hp']]", system_text)
        self.assertIn("AP %d / %d", system_text)
        self.assertNotIn("MP --", system_text)
        self.assertIn("STA %d / %d", system_text)
        self.assertIn("CHAOS %d / %d", system_text)

    def test_player_sprite_has_clickable_quick_actions(self):
        system_text = TURN_BATTLE_SYSTEM_FILE.read_text()

        self.assertIn("use turn_battle_player_action_hotspot(player, outcome)", system_text)
        self.assertIn("screen turn_battle_player_action_hotspot(player, outcome):", system_text)
        self.assertIn('action ToggleScreen("turn_battle_player_quick_actions")', system_text)
        self.assertIn("screen turn_battle_player_quick_actions():", system_text)
        self.assertIn("xalign 0.78", system_text)
        self.assertIn("yalign 0.64", system_text)
        self.assertIn("zoom 0.92", system_text)
        self.assertIn('action [Hide("turn_battle_player_quick_actions"), Return(action_id)]', system_text)
        self.assertIn('label=turn_battle_action_label("attack")', system_text)
        self.assertIn('label=turn_battle_action_label("ember_focus")', system_text)
        self.assertIn('label=turn_battle_action_label("focus")', system_text)
        self.assertIn('label="Qana"', system_text)
        self.assertIn('label=turn_battle_action_label("fire_ball")', system_text)
        self.assertIn('label=turn_battle_action_label("healing_burst")', system_text)
        self.assertIn('label=turn_battle_action_label("freeze_ray")', system_text)
        self.assertIn('label="Dragon Spells"', system_text)
        self.assertIn('label=turn_battle_action_label("dragon_geisure")', system_text)
        self.assertIn('label=turn_battle_action_label("dragon_javelin")', system_text)
        self.assertIn('label=turn_battle_action_label("health_elixir")', system_text)
        self.assertIn('label=turn_battle_action_label("qana_elixir")', system_text)
        self.assertIn('label=turn_battle_action_label("guard")', system_text)
        self.assertIn('label=turn_battle_action_label("dodge")', system_text)
        self.assertIn("xpos turn_battle_hotspot_x(player)", system_text)
        self.assertIn("ypos turn_battle_hotspot_y(player)", system_text)
        self.assertIn("turn_battle_dragon_spells_enabled", system_text)
        self.assertIn("xsize 220", system_text)
        self.assertIn("ysize 310", system_text)

    def test_training_encounter_defines_placeholder_sprites(self):
        encounter = combat_data.BATTLE_ENCOUNTERS["meditation_dummy"]

        self.assertEqual(encounter["background"], "bg severance dark")
        self.assertEqual(encounter["party"][0]["id"], "oren")
        self.assertEqual(encounter["party"][0]["max_ap"], 5)
        self.assertEqual(encounter["party"][0]["max_qana"], 10)
        self.assertEqual(encounter["party"][0]["max_stamina"], 6)
        self.assertEqual(encounter["party"][0]["max_chaos"], 10)
        self.assertEqual(encounter["enemy"]["max_ap"], 5)
        self.assertEqual(encounter["enemy"]["max_qana"], 8)
        self.assertEqual(encounter["enemy"]["max_stamina"], 4)
        self.assertEqual(encounter["enemy"]["actions"], ["freeze_ray"])
        self.assertEqual(encounter["enemy"]["attack_cost"], 1)
        self.assertEqual(encounter["actions"]["attack"]["cost"], 2)
        self.assertEqual(encounter["actions"]["attack"]["label"], "Basic Attack")
        self.assertEqual(encounter["actions"]["attack"]["uses_per_round"], 5)
        self.assertEqual(encounter["actions"]["focus"]["restores_ap"], 3)
        self.assertEqual(encounter["actions"]["focus"]["label"], "AP Recovery")
        self.assertEqual(encounter["actions"]["focus"]["uses_per_round"], 1)
        self.assertEqual(encounter["actions"]["ember_focus"]["label"], "Ultimate")
        self.assertEqual(encounter["actions"]["ember_focus"]["cost"], 5)
        self.assertEqual(encounter["actions"]["fire_ball"]["label"], "Fire Ball I")
        self.assertEqual(encounter["actions"]["fire_ball"]["base_label"], "Fire Ball")
        self.assertEqual(encounter["actions"]["fire_ball"]["tier"], 1)
        self.assertIn(3, encounter["actions"]["fire_ball"]["tiers"])
        self.assertEqual(encounter["actions"]["fire_ball"]["cost"], 2)
        self.assertEqual(encounter["actions"]["fire_ball"]["tick_rounds"], 3)
        self.assertEqual(encounter["actions"]["healing_burst"]["label"], "Healing Burst I")
        self.assertEqual(encounter["actions"]["healing_burst"]["cost"], 2)
        self.assertEqual(encounter["actions"]["freeze_ray"]["label"], "Freeze Ray I")
        self.assertEqual(encounter["actions"]["freeze_ray"]["cost"], 3)
        self.assertEqual(encounter["actions"]["freeze_ray"]["freeze_rounds"], 2)
        self.assertEqual(encounter["actions"]["dragon_geisure"]["label"], "Dragon Geisure I")
        self.assertEqual(encounter["actions"]["dragon_geisure"]["cost"], 5)
        self.assertEqual(encounter["actions"]["dragon_geisure"]["max_targets"], 5)
        self.assertEqual(encounter["actions"]["dragon_geisure"]["chaos_gain"], 5)
        self.assertEqual(encounter["actions"]["dragon_javelin"]["label"], "Dragon Javelin I")
        self.assertEqual(encounter["actions"]["dragon_javelin"]["cost"], 5)
        self.assertEqual(encounter["actions"]["dragon_javelin"]["pierce_chance"], 0.2)
        self.assertEqual(encounter["actions"]["dragon_javelin"]["chaos_gain"], 4)
        self.assertEqual(encounter["actions"]["health_elixir"]["starting_uses"], 1)
        self.assertEqual(encounter["actions"]["health_elixir"]["use_capacity"], 2)
        self.assertEqual(encounter["actions"]["qana_elixir"]["restores_qana"], 3)
        self.assertEqual(encounter["actions"]["guard"]["cost"], 0)
        self.assertEqual(encounter["actions"]["guard"]["label"], "Block")
        self.assertEqual(encounter["actions"]["guard"]["stamina_cost"], 2)
        self.assertEqual(encounter["actions"]["dodge"]["stamina_cost"], 2)
        self.assertAlmostEqual(encounter["actions"]["dodge"]["dodge_chance"], 0.667)
        self.assertNotIn("uses_per_round", encounter["actions"]["guard"])
        self.assertEqual(encounter["party"][0]["sprite"], "combat oren idle")
        self.assertEqual(encounter["enemy"]["sprite"], "combat training dummy temp idle")

        team_encounter = combat_data.BATTLE_ENCOUNTERS["team_dummy"]
        self.assertTrue(team_encounter["controlled_party_turns"])
        self.assertEqual(team_encounter["party"][1]["sprite"], "combat ally dummy temp idle")
        self.assertEqual(team_encounter["party"][1]["max_hp"], 28)
        self.assertEqual(team_encounter["party"][1]["max_ap"], 5)
        self.assertEqual(team_encounter["party"][1]["actions"], encounter["party"][0]["actions"])
        self.assertTrue(encounter["party"][0]["allow_dragon_spells"])
        self.assertNotIn("allow_dragon_spells", team_encounter["party"][1])

    def test_temp_combat_sprite_assets_are_registered(self):
        images_text = IMAGES_FILE.read_text()

        self.assertIn(
            'image combat oren temp idle = "images/combat/oren_temp_idle.png"',
            images_text,
        )
        self.assertIn("image combat oren idle:", images_text)
        self.assertIn('"images/combat/oren/idle_00.png"', images_text)
        self.assertIn('"images/combat/oren/idle_07.png"', images_text)
        self.assertIn("pause 0.36", images_text)
        self.assertIn(
            'image combat training dummy temp idle = "images/combat/training_dummy_temp_idle.png"',
            images_text,
        )
        self.assertIn(
            'image combat ally dummy temp idle = "images/combat/ally_dummy_temp_idle.png"',
            images_text,
        )
        self.assertTrue((GAME_ROOT / "images" / "combat" / "oren_temp_idle.png").exists())
        self.assertTrue((GAME_ROOT / "images" / "combat" / "oren" / "idle_00.png").exists())
        self.assertTrue((GAME_ROOT / "images" / "combat" / "oren" / "idle_07.png").exists())
        self.assertTrue((GAME_ROOT / "images" / "combat" / "training_dummy_temp_idle.png").exists())
        self.assertTrue((GAME_ROOT / "images" / "combat" / "ally_dummy_temp_idle.png").exists())


if __name__ == "__main__":
    unittest.main()
