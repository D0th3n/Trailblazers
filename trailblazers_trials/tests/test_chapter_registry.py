from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_FILE = PROJECT_ROOT / "game" / "chapter_registry.py"


def load_chapter_registry():
    spec = spec_from_file_location("chapter_registry", MODULE_FILE)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ChapterRegistryTests(unittest.TestCase):

    def test_featured_chapter_is_available_and_named(self):
        chapter_registry = load_chapter_registry()

        featured = chapter_registry.featured_chapter()

        self.assertTrue(featured["available"])
        self.assertEqual(featured["id"], "chapter_01")
        self.assertEqual(featured["title"], "Heart of Fire")

    def test_checkpoint_entries_include_chapter_metadata(self):
        chapter_registry = load_chapter_registry()

        checkpoints = chapter_registry.checkpoint_entries()

        self.assertGreaterEqual(len(checkpoints), 3)
        self.assertEqual(checkpoints[0]["chapter_id"], "chapter_01")
        self.assertEqual(checkpoints[0]["chapter_number"], "Chapter 1")
        self.assertEqual(checkpoints[0]["chapter_title"], "Heart of Fire")

    def test_playable_label_set_contains_start_and_checkpoints(self):
        chapter_registry = load_chapter_registry()

        playable_labels = chapter_registry.playable_label_set()

        self.assertIn("chapter_01", playable_labels)
        self.assertIn("chapter_01_checkpoint_evening", playable_labels)
        self.assertIn("chapter_01_checkpoint_mine", playable_labels)

    def test_chapter_two_is_registered_with_independent_routes(self):
        chapter_registry = load_chapter_registry()

        chapters = chapter_registry.chapter_card_entries()
        chapter_two = next((chapter for chapter in chapters if chapter["id"] == "chapter_02"), None)

        self.assertIsNotNone(chapter_two)
        self.assertEqual(chapter_two["number"], "Chapter 2")
        self.assertEqual(chapter_two["roman"], "Chapter II")
        self.assertEqual(chapter_two["start_label"], "chapter_02")
        self.assertNotEqual(chapters[0]["start_label"], chapter_two["start_label"])
        self.assertEqual(
            [checkpoint["label"] for checkpoint in chapter_two["checkpoints"]],
            [
                "chapter_02",
                "chapter_02_checkpoint_evening",
                "chapter_02_checkpoint_mine",
            ],
        )


if __name__ == "__main__":
    unittest.main()
