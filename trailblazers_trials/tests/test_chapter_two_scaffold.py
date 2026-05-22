from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHAPTER_ONE_FILE = PROJECT_ROOT / "game" / "chapters" / "chapter_01.rpy"
CHAPTER_TWO_FILE = PROJECT_ROOT / "game" / "chapters" / "chapter_02.rpy"
VARIABLES_FILE = PROJECT_ROOT / "game" / "variables.rpy"
EXPLORATION_DATA_FILE = PROJECT_ROOT / "game" / "exploration_data.py"


class ChapterTwoScaffoldTests(unittest.TestCase):

    def test_chapter_two_file_has_independent_labels(self):
        chapter_two_text = CHAPTER_TWO_FILE.read_text()

        self.assertIn("label chapter_02:", chapter_two_text)
        self.assertIn("label chapter_02_checkpoint_evening:", chapter_two_text)
        self.assertIn("label chapter_02_checkpoint_mine:", chapter_two_text)
        self.assertIn("label chapter_02_anozira_square_exploration:", chapter_two_text)
        self.assertIn("label chapter_02_anozira_evening_interlude:", chapter_two_text)
        self.assertIn("label chapter_02_ruzen_mine_approach:", chapter_two_text)
        self.assertIn("jump chapter_02", chapter_two_text)
        self.assertNotIn("jump chapter_01", chapter_two_text)
        self.assertNotIn("call anozira_square_exploration", chapter_two_text)
        self.assertNotIn("call anozira_evening_interlude", chapter_two_text)
        self.assertNotIn("call ruzen_mine_approach", chapter_two_text)

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

    def test_chapter_two_uses_separate_progression_state(self):
        variables_text = VARIABLES_FILE.read_text()
        chapter_two_text = CHAPTER_TWO_FILE.read_text()
        exploration_data_text = EXPLORATION_DATA_FILE.read_text()

        for flag_name in (
            "chapter_02_ruzen_lead_unlocked",
            "chapter_02_visited_village_exploration",
            "chapter_02_village_square_exploration_complete",
            "chapter_02_explored_village_well",
            "chapter_02_explored_village_rumor",
            "chapter_02_visited_tavern",
            "chapter_02_heard_dead_miner_hint",
            "chapter_02_mine_tampering_suspected",
            "chapter_02_mogul_encountered",
            "chapter_02_titan_pressure_felt",
            "chapter_02_titan_revealed",
            "chapter_02_titan_destroyed",
        ):
            self.assertIn("default %s" % flag_name, variables_text)
            self.assertIn(flag_name, chapter_two_text)

        self.assertIn('"chapter_02_anozira_square"', exploration_data_text)
        self.assertIn('"well": "chapter_02_explored_village_well"', exploration_data_text)
        self.assertIn('"villager": "chapter_02_explored_village_rumor"', exploration_data_text)
        self.assertIn('exploration_begin("chapter_02_anozira_square"', chapter_two_text)


if __name__ == "__main__":
    unittest.main()
