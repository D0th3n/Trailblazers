from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHAPTER_FILE = PROJECT_ROOT / "game" / "chapters" / "chapter_01.rpy"
SCREENS_FILE = PROJECT_ROOT / "game" / "screens.rpy"


class ChapterCompletionTests(unittest.TestCase):

    def test_chapter_one_ends_with_completion_screen_and_routing(self):
        chapter_text = CHAPTER_FILE.read_text()

        self.assertIn("call screen chapter_complete_menu(", chapter_text)
        self.assertIn('chapter_title="Heart of Fire"', chapter_text)
        self.assertIn('_return == "replay"', chapter_text)
        self.assertIn("jump chapter_01", chapter_text)
        self.assertIn('_return == "chapter_select"', chapter_text)
        self.assertIn('startup_destination = "chapter_select"', chapter_text)
        self.assertIn("jump start", chapter_text)

    def test_completion_screen_exposes_replay_chapters_and_title_actions(self):
        screens_text = SCREENS_FILE.read_text()

        self.assertIn("screen chapter_complete_menu(", screens_text)
        self.assertIn('textbutton "Replay Chapter"', screens_text)
        self.assertIn('textbutton "Chapters"', screens_text)
        self.assertIn('textbutton "Title Menu"', screens_text)
        self.assertIn('add Transform("cg anozira thanks ending"', screens_text)


if __name__ == "__main__":
    unittest.main()
