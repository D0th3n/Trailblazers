from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_FILE = PROJECT_ROOT / "game" / "menu_support.py"


def load_menu_support():
    spec = spec_from_file_location("menu_support", MODULE_FILE)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MenuSupportTests(unittest.TestCase):

    def test_world_history_overview_mentions_core_world_context(self):
        menu_support = load_menu_support()

        self.assertIn("Qana", menu_support.WORLD_HISTORY_OVERVIEW)
        self.assertIn("Acerima", menu_support.WORLD_HISTORY_OVERVIEW)
        self.assertIn("dragons", menu_support.WORLD_HISTORY_OVERVIEW.lower())

    def test_submit_issue_report_writes_jsonl_record(self):
        menu_support = load_menu_support()

        with TemporaryDirectory() as temp_dir:
            report_path = menu_support.submit_issue_report(
                temp_dir,
                "Menu marker click issue",
                "The main quest marker should match the well marker style.",
                player_name="Murks",
            )

            self.assertTrue(Path(report_path).exists())
            report_text = Path(report_path).read_text()
            self.assertIn("Menu marker click issue", report_text)
            self.assertIn("Murks", report_text)


if __name__ == "__main__":
    unittest.main()
