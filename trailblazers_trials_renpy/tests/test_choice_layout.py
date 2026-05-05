from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCREENS_FILE = PROJECT_ROOT / "game" / "screens.rpy"


class ChoiceLayoutTests(unittest.TestCase):

    def test_custom_choice_screen_uses_top_panel_background(self):
        screens_text = SCREENS_FILE.read_text()

        self.assertIn("screen choice(items):", screens_text)
        self.assertIn('style_prefix "choice"', screens_text)
        self.assertIn('add Solid("#130905d8")', screens_text)
        self.assertIn("xsize TB_SCREEN_W", screens_text)
        self.assertIn("ysize 220", screens_text)
        self.assertIn("xpos 40", screens_text)
        self.assertIn("ypos 24", screens_text)
        self.assertIn("style choice_button is button", screens_text)
        self.assertIn("style choice_button_text is text", screens_text)


if __name__ == "__main__":
    unittest.main()
