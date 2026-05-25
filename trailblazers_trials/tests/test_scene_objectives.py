from pathlib import Path
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = PROJECT_ROOT / "game"
CHAPTER_TWO_FILE = GAME_ROOT / "chapters" / "chapter_02.rpy"
VARIABLES_FILE = GAME_ROOT / "variables.rpy"
SCENE_OBJECTIVE_SYSTEM_FILE = GAME_ROOT / "systems" / "scene_objectives.rpy"
if str(GAME_ROOT) not in sys.path:
    sys.path.insert(0, str(GAME_ROOT))


import scene_objectives
import scene_objectives_data


class SceneObjectiveTests(unittest.TestCase):

    def setUp(self):
        self.scene = scene_objectives_data.INTERACTIVE_SCENES["chapter_02_room"]

    def test_door_is_blocked_until_oren_gets_dressed(self):
        state = scene_objectives.hotspot_state(self.scene, "door", completed_actions=[])

        self.assertFalse(state["enabled"])
        self.assertEqual(
            state["message"],
            "I should get dressed before I leave.",
        )

    def test_dresser_is_available_before_oren_gets_dressed(self):
        state = scene_objectives.hotspot_state(self.scene, "dresser", completed_actions=[])

        self.assertTrue(state["enabled"])
        self.assertIsNone(state["message"])

    def test_door_is_available_after_oren_gets_dressed(self):
        state = scene_objectives.hotspot_state(
            self.scene,
            "door",
            completed_actions=["get_dressed"],
        )

        self.assertTrue(state["enabled"])
        self.assertIsNone(state["message"])

    def test_completed_hotspots_are_hidden(self):
        visible = scene_objectives.visible_hotspot_ids(
            self.scene,
            completed_actions=["get_dressed"],
        )

        self.assertNotIn("dresser", visible)
        self.assertIn("door", visible)

    def test_scene_is_complete_when_required_actions_are_done(self):
        self.assertFalse(
            scene_objectives.scene_complete(self.scene, completed_actions=[])
        )
        self.assertTrue(
            scene_objectives.scene_complete(
                self.scene,
                completed_actions=["get_dressed"],
            )
        )


class SceneObjectiveRenpyIntegrationTests(unittest.TestCase):

    def test_scene_objective_runtime_imports_data_and_model(self):
        system_text = SCENE_OBJECTIVE_SYSTEM_FILE.read_text()

        self.assertIn("import scene_objectives", system_text)
        self.assertIn("import scene_objectives_data", system_text)
        self.assertIn("def scene_objective_begin(scene_id):", system_text)
        self.assertIn("def scene_objective_complete_action(action_id):", system_text)
        self.assertIn("screen scene_objective_hotspots():", system_text)
        self.assertIn("action Return(hotspot_id)", system_text)

    def test_chapter_two_uses_room_objective_before_hallway(self):
        chapter_two_text = CHAPTER_TWO_FILE.read_text()

        self.assertIn("label chapter_02_room_objective:", chapter_two_text)
        self.assertIn('scene_objective_begin("chapter_02_room")', chapter_two_text)
        self.assertIn("call screen scene_objective_hotspots", chapter_two_text)
        self.assertIn('if chapter_02_room_choice == "dresser":', chapter_two_text)
        self.assertIn('if chapter_02_room_choice == "door":', chapter_two_text)
        self.assertIn('oren annoyed "I should get dressed before I leave."', chapter_two_text)
        self.assertLess(
            chapter_two_text.index("jump chapter_02_room_objective"),
            chapter_two_text.index("label chapter_02_armoring:"),
        )

    def test_scene_objective_state_is_saveable(self):
        variables_text = VARIABLES_FILE.read_text()

        self.assertIn("default scene_objective_scene_id = None", variables_text)
        self.assertIn("default scene_objective_completed_actions = []", variables_text)


if __name__ == "__main__":
    unittest.main()
