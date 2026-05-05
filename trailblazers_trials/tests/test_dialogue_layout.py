from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCREENS_FILE = PROJECT_ROOT / "game" / "screens.rpy"


class DialogueLayoutTests(unittest.TestCase):

    def test_custom_say_screen_uses_top_background_panel(self):
        screens_text = SCREENS_FILE.read_text()

        self.assertIn("screen say(who, what):", screens_text)
        self.assertIn('id "window"', screens_text)
        self.assertIn('style "say_window"', screens_text)
        self.assertIn('background Solid("#120a08d6")', screens_text)
        self.assertIn("xpos 20", screens_text)
        self.assertIn("ypos 18", screens_text)
        self.assertIn('style "say_dialogue"', screens_text)
        self.assertIn('style "say_label"', screens_text)


if __name__ == "__main__":
    unittest.main()
