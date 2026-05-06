from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "game"
if str(GAME_DIR) not in sys.path:
    sys.path.insert(0, str(GAME_DIR))


from hotspot_scene_data import HOTSPOT_SCENE_REGISTRY, SCREEN_H, SCREEN_W
from hotspot_scene_model import (
    available_hotspots,
    validate_hotspot_registry,
    validate_hotspot_scene,
)


class HotspotSceneModelTests(unittest.TestCase):

    def test_shared_hotspot_registry_uses_standard_canvas_size(self):
        self.assertEqual(SCREEN_W, 1600)
        self.assertEqual(SCREEN_H, 900)

    def test_shared_hotspot_registry_includes_expected_scenes(self):
        self.assertEqual(
            set(HOTSPOT_SCENE_REGISTRY.keys()),
            {"anozira_overview", "tavern_room"},
        )

    def test_available_hotspots_filters_by_unlock_flags(self):
        scene = HOTSPOT_SCENE_REGISTRY["anozira_overview"]

        self.assertEqual(
            [hotspot["id"] for hotspot in available_hotspots(scene, set())],
            ["well", "villager", "market_day"],
        )
        self.assertEqual(
            [hotspot["id"] for hotspot in available_hotspots(scene, {"tavern_unlocked"})],
            ["well", "villager", "market_day", "tavern"],
        )
        self.assertEqual(
            [
                hotspot["id"]
                for hotspot in available_hotspots(
                    scene,
                    {"tavern_unlocked", "mine_unlocked"},
                )
            ],
            ["well", "villager", "market_day", "tavern", "mine_path"],
        )

    def test_validate_hotspot_scene_accepts_shared_registry_scenes(self):
        for scene in HOTSPOT_SCENE_REGISTRY.values():
            self.assertEqual(validate_hotspot_scene(scene), [])

    def test_validate_hotspot_scene_reports_missing_background_and_hotspots(self):
        problems = validate_hotspot_scene(
            {
                "scene_id": "broken",
                "title": "Broken",
                "objective": "Broken",
                "hotspots": [],
            }
        )

        self.assertIn("missing_background", problems)
        self.assertIn("missing_hotspots", problems)

    def test_validate_hotspot_scene_reports_out_of_bounds_hotspots(self):
        problems = validate_hotspot_scene(
            {
                "scene_id": "broken",
                "background": "bg broken",
                "title": "Broken",
                "objective": "Broken",
                "hotspots": [
                    {
                        "id": "too_far_right",
                        "label": "Too Far Right",
                        "x": 1600,
                        "y": 100,
                    }
                ],
            }
        )

        self.assertIn("hotspot_out_of_bounds:too_far_right", problems)

    def test_validate_hotspot_registry_prefixes_scene_ids_on_problems(self):
        registry = {
            "broken_scene": {
                "background": "",
                "title": "Broken",
                "objective": "Broken",
                "hotspots": [],
            }
        }

        self.assertEqual(
            validate_hotspot_registry(registry),
            [
                "broken_scene:missing_background",
                "broken_scene:missing_hotspots",
            ],
        )


if __name__ == "__main__":
    unittest.main()
