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

    def test_chapter_select_brute_forces_visible_chapter_cards(self):
        screens_text = SCREENS_FILE.read_text()
        start = screens_text.index("screen chapter_select_menu(")
        end = screens_text.index("screen title_load_menu(", start)
        chapter_select_text = screens_text[start:end]

        self.assertIn("screen chapter_select_menu(", chapter_select_text)
        self.assertIn('$ chapter_01_action = Return("chapter_01") if startup_mode else Start("chapter_01")', chapter_select_text)
        self.assertIn('$ chapter_02_action = Return("chapter_02") if startup_mode else Start("chapter_02")', chapter_select_text)
        self.assertIn('text "Chapter 1":', chapter_select_text)
        self.assertIn('text "Chapter 2":', chapter_select_text)
        self.assertIn('text "Heart of Fire":', chapter_select_text)
        self.assertIn('text "Oren Gets Ready":', chapter_select_text)
        self.assertIn("action chapter_01_action", chapter_select_text)
        self.assertIn("action chapter_02_action", chapter_select_text)
        self.assertNotIn("vpgrid:", chapter_select_text)
        self.assertNotIn("id \"chapter_select_grid\"", chapter_select_text)
        self.assertNotIn("chapter_card_entries()", chapter_select_text)


if __name__ == "__main__":
    unittest.main()
