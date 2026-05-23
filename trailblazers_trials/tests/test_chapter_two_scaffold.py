from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHAPTER_ONE_FILE = PROJECT_ROOT / "game" / "chapters" / "chapter_01.rpy"
CHAPTER_TWO_FILE = PROJECT_ROOT / "game" / "chapters" / "chapter_02.rpy"
VARIABLES_FILE = PROJECT_ROOT / "game" / "variables.rpy"
IMAGES_FILE = PROJECT_ROOT / "game" / "images.rpy"


class ChapterTwoScaffoldTests(unittest.TestCase):

    def test_chapter_two_file_has_independent_labels(self):
        chapter_two_text = CHAPTER_TWO_FILE.read_text()

        self.assertIn("label chapter_02:", chapter_two_text)
        self.assertIn("label chapter_02_checkpoint_evening:", chapter_two_text)
        self.assertIn("label chapter_02_checkpoint_mine:", chapter_two_text)
        self.assertIn("jump chapter_02", chapter_two_text)
        self.assertNotIn("jump chapter_01", chapter_two_text)
        self.assertNotIn("call anozira_square_exploration", chapter_two_text)
        self.assertNotIn("call anozira_evening_interlude", chapter_two_text)
        self.assertNotIn("call ruzen_mine_approach", chapter_two_text)
        self.assertNotIn("label chapter_02_anozira_square_exploration:", chapter_two_text)
        self.assertNotIn("label chapter_02_anozira_evening_interlude:", chapter_two_text)
        self.assertNotIn("label chapter_02_ruzen_mine_approach:", chapter_two_text)

    def test_chapter_one_keeps_original_labels(self):
        chapter_one_text = CHAPTER_ONE_FILE.read_text()

        self.assertIn("label chapter_01:", chapter_one_text)
        self.assertIn("label anozira_square_exploration:", chapter_one_text)
        self.assertIn("label anozira_evening_interlude:", chapter_one_text)
        self.assertIn("label ruzen_mine_approach:", chapter_one_text)
        self.assertNotIn("label chapter_02:", chapter_one_text)

    def test_chapter_two_uses_separate_placeholder_result_state(self):
        variables_text = VARIABLES_FILE.read_text()
        chapter_two_text = CHAPTER_TWO_FILE.read_text()

        self.assertIn('default chapter_02_result = "unresolved"', variables_text)
        self.assertIn("chapter_02_result", chapter_two_text)
        self.assertNotIn("chapter_01_result", chapter_two_text)

    def test_chapter_two_is_short_oren_getting_ready_placeholder(self):
        chapter_two_text = CHAPTER_TWO_FILE.read_text()

        self.assertIn("scene cg chapter_02_oren_waking", chapter_two_text)
        self.assertIn("scene cg chapter_02_oren_armoring", chapter_two_text)
        self.assertIn("scene cg chapter_02_oren_hallway", chapter_two_text)
        self.assertIn("Oren sat up before the inn bell finished its first ring.", chapter_two_text)
        self.assertIn("The armor waited across the blanket like a promise he had not agreed to keep.", chapter_two_text)
        self.assertIn("call screen chapter_complete_menu(", chapter_two_text)
        self.assertIn('chapter_title="Oren Gets Ready"', chapter_two_text)
        self.assertNotIn("call simple_battle_preview", chapter_two_text)
        self.assertNotIn("exploration_begin(", chapter_two_text)
        self.assertNotIn("Moglim", chapter_two_text)

    def test_chapter_two_images_are_registered(self):
        images_text = IMAGES_FILE.read_text()

        self.assertIn('image cg chapter_02_oren_waking = "images/cg/chapter_02/oren_waking.png"', images_text)
        self.assertIn('image cg chapter_02_oren_armoring = "images/cg/chapter_02/oren_armoring.png"', images_text)
        self.assertIn('image cg chapter_02_oren_hallway = "images/cg/chapter_02/oren_hallway.png"', images_text)


if __name__ == "__main__":
    unittest.main()
