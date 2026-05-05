from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GUI_FILE = PROJECT_ROOT / "game" / "gui.rpy"
SCREENS_FILE = PROJECT_ROOT / "game" / "screens.rpy"


class MenuLayoutTests(unittest.TestCase):

    def test_game_uses_larger_base_resolution(self):
        gui_text = GUI_FILE.read_text()

        self.assertIn("gui.init(1600, 900)", gui_text)

    def test_menu_avoids_old_small_fixed_canvas_values(self):
        screens_text = SCREENS_FILE.read_text()

        self.assertNotIn("xysize=(1280, 720)", screens_text)
        self.assertNotIn("xsize 900", screens_text)
        self.assertNotIn("ysize 600", screens_text)
        self.assertNotIn("xpos 355", screens_text)
        self.assertIn("TB_SCREEN_W = 1600", screens_text)
        self.assertIn("TB_SCREEN_H = 900", screens_text)
        self.assertIn("TB_SURFACE_W =", screens_text)
        self.assertIn("TB_SURFACE_X =", screens_text)


if __name__ == "__main__":
    unittest.main()
