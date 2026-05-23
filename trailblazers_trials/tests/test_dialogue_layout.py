from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCREENS_FILE = PROJECT_ROOT / "game" / "screens.rpy"
IMAGES_FILE = PROJECT_ROOT / "game" / "images.rpy"
CHARACTERS_FILE = PROJECT_ROOT / "game" / "characters.rpy"
CHAPTER_TWO_FILE = PROJECT_ROOT / "game" / "chapters" / "chapter_02.rpy"
VARIABLES_FILE = PROJECT_ROOT / "game" / "variables.rpy"


class DialogueLayoutTests(unittest.TestCase):

    def test_custom_say_screen_uses_bottom_dialogue_bar_with_side_portrait(self):
        screens_text = SCREENS_FILE.read_text()

        self.assertIn("screen say(who, what):", screens_text)
        self.assertIn('id "window"', screens_text)
        self.assertIn('style "say_window"', screens_text)
        self.assertIn("add SideImage()", screens_text)
        self.assertIn("style \"say_side_image_frame\"", screens_text)
        self.assertIn("xpos 24", screens_text)
        self.assertIn("yalign 1.0", screens_text)
        self.assertIn("yoffset -42", screens_text)
        self.assertIn('style "say_dialogue"', screens_text)
        self.assertIn('style "say_label"', screens_text)
        self.assertIn('background Solid("#050506b8")', screens_text)
        self.assertIn("xfill True", screens_text)
        self.assertIn("xmaximum 1220", screens_text)
        self.assertIn("use dialogue_controls", screens_text)

    def test_dialogue_controls_match_reference_controls(self):
        screens_text = SCREENS_FILE.read_text()

        self.assertIn("screen dialogue_controls():", screens_text)

        expected_controls = {
            'textbutton _("Back")': "Rollback()",
            'textbutton _("History")': 'ShowMenu("history")',
            'textbutton _("Skip")': "Return()",
            'textbutton _("Auto")': 'ToggleVariable("tb_auto_advance")',
            'textbutton _("Save")': 'ShowMenu("save")',
            'textbutton _("Q.Save")': "QuickSave()",
            'textbutton _("Q.Load")': "QuickLoad()",
            'textbutton _("Prefs")': 'ShowMenu("preferences")',
        }

        for label, action in expected_controls.items():
            self.assertIn(label, screens_text)
            self.assertIn("action %s" % action, screens_text)

        self.assertIn('style "dialogue_controls_hbox"', screens_text)
        self.assertIn("style dialogue_control_button_text", screens_text)

    def test_auto_control_advances_dialogue_every_three_seconds(self):
        screens_text = SCREENS_FILE.read_text()
        variables_text = VARIABLES_FILE.read_text()

        self.assertIn("default tb_auto_advance = False", variables_text)
        self.assertIn("if tb_auto_advance:", screens_text)
        self.assertIn("timer 3.0 action Return()", screens_text)
        self.assertNotIn('action Preference("auto-forward", "toggle")', screens_text)
        self.assertNotIn("action Skip()", screens_text)

    def test_oren_side_portraits_are_registered(self):
        images_text = IMAGES_FILE.read_text()
        characters_text = CHARACTERS_FILE.read_text()

        self.assertIn('define oren = Character("Oren", color="#f0c36a", image="oren")', characters_text)

        for expression in ("neutral", "focused", "annoyed", "uneasy", "confident"):
            self.assertIn(
                'image side oren %s = "images/characters/side/oren_%s.png"' % (expression, expression),
                images_text,
            )

    def test_chapter_two_tags_oren_dialogue_with_emotions(self):
        chapter_two_text = CHAPTER_TWO_FILE.read_text()

        self.assertIn('oren focused "One more assignment.', chapter_two_text)
        self.assertIn('oren annoyed "That was not encouragement.', chapter_two_text)
        self.assertIn('oren focused "Left strap first.', chapter_two_text)
        self.assertIn('oren confident "Then today I use the cage.', chapter_two_text)
        self.assertIn('oren neutral "Good morning.', chapter_two_text)


if __name__ == "__main__":
    unittest.main()
