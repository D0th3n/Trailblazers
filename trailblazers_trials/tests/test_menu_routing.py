from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_FILE = PROJECT_ROOT / "game" / "script.rpy"
SCREENS_FILE = PROJECT_ROOT / "game" / "screens.rpy"
AUDIO_FILE = PROJECT_ROOT / "game" / "audio.rpy"


class MenuRoutingTests(unittest.TestCase):

    def test_start_label_routes_all_title_menu_sections(self):
        script_text = SCRIPT_FILE.read_text()

        self.assertIn("label start:", script_text)
        self.assertIn("import chapter_registry", script_text)
        self.assertIn('default startup_destination = "main"', script_text)
        self.assertIn("play music title_menu_theme fadeout 1.0 fadein 1.0", script_text)
        self.assertIn("call screen startup_main_menu", script_text)
        self.assertIn('startup_destination == "history"', script_text)
        self.assertIn("call screen history_menu", script_text)
        self.assertIn('startup_destination == "chapter_select"', script_text)
        self.assertIn("call screen chapter_select_menu", script_text)
        self.assertIn("startup_mode=True", script_text)
        self.assertIn('startup_destination == "load"', script_text)
        self.assertIn("call screen title_load_menu", script_text)
        self.assertIn('startup_destination == "preferences"', script_text)
        self.assertIn("call screen title_preferences_menu", script_text)
        self.assertIn('startup_destination == "about"', script_text)
        self.assertIn("call screen about_menu", script_text)
        self.assertIn('startup_destination == "help"', script_text)
        self.assertIn("call screen help_menu", script_text)
        self.assertIn('startup_destination == "quit"', script_text)
        self.assertIn("call screen quit_confirm_menu", script_text)
        self.assertIn("chapter_registry.playable_label_set()", script_text)
        self.assertIn("call expression _return", script_text)
        self.assertIn('startup_destination = _return', script_text)
        self.assertIn('startup_destination = "main"', script_text)
        self.assertNotIn("jump _main_menu", script_text)

    def test_title_navigation_and_menu_screens_use_registry_backed_chapter_data(self):
        screens_text = SCREENS_FILE.read_text()

        self.assertIn("import chapter_registry", screens_text)
        self.assertIn("screen navigation(", screens_text)
        self.assertIn("title_mode=False", screens_text)
        self.assertIn("if title_mode:", screens_text)
        self.assertIn('textbutton _("History")', screens_text)
        self.assertIn('textbutton _("Chapters")', screens_text)
        self.assertIn('textbutton _("Load")', screens_text)
        self.assertIn('textbutton _("Preferences")', screens_text)
        self.assertIn('textbutton _("About")', screens_text)
        self.assertIn('textbutton _("Help")', screens_text)
        self.assertIn('textbutton _("Quit")', screens_text)
        self.assertIn("title_mode=True,", screens_text)
        self.assertIn("$ featured = featured_chapter()", screens_text)
        self.assertIn("screen chapter_select_menu(", screens_text)
        self.assertIn('$ chapter_01_action = Return("chapter_01") if startup_mode else Start("chapter_01")', screens_text)
        self.assertIn('$ chapter_02_action = Return("chapter_02") if startup_mode else Start("chapter_02")', screens_text)
        self.assertIn("action chapter_01_action", screens_text)
        self.assertIn("action chapter_02_action", screens_text)
        self.assertIn("screen history_menu(", screens_text)
        self.assertIn("screen title_load_menu(", screens_text)
        self.assertIn("$ checkpoints = checkpoint_entries()", screens_text)
        self.assertIn("for checkpoint in checkpoints:", screens_text)
        self.assertIn('$ checkpoint_action = Return(checkpoint["label"]) if startup_mode else Start(checkpoint["label"])', screens_text)
        self.assertIn("action checkpoint_action", screens_text)
        self.assertIn("screen title_preferences_menu(", screens_text)
        self.assertIn("screen about_menu(", screens_text)
        self.assertIn("screen help_menu(", screens_text)
        self.assertIn("screen quit_confirm_menu(", screens_text)
        self.assertNotIn("chapter_01_action=Start(", screens_text)
        self.assertNotIn("chapter_01_evening_action=Start(", screens_text)
        self.assertNotIn("chapter_01_mine_action=Start(", screens_text)

    def test_title_menu_music_is_registered(self):
        audio_text = AUDIO_FILE.read_text()

        self.assertIn('define audio.title_menu_theme = "audio/menu/trombone_glitch.wav"', audio_text)


if __name__ == "__main__":
    unittest.main()
