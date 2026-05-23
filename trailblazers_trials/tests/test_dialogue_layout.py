from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCREENS_FILE = PROJECT_ROOT / "game" / "screens.rpy"
IMAGES_FILE = PROJECT_ROOT / "game" / "images.rpy"
CHARACTERS_FILE = PROJECT_ROOT / "game" / "characters.rpy"
CHAPTER_TWO_FILE = PROJECT_ROOT / "game" / "chapters" / "chapter_02.rpy"


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
