from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "game"
if str(GAME_DIR) not in sys.path:
    sys.path.insert(0, str(GAME_DIR))


from exploration_data import EXPLORATION_MAPS
from exploration_model import (
    find_event,
    format_quest_log_entry,
    marker_anchor,
    move_position,
    shortest_path,
    shortest_path_length,
    tile_to_pixels,
    validate_map_data,
)


class ExplorationModelTests(unittest.TestCase):

    def test_move_position_advances_on_open_tile(self):
        position = (3, 4)
        blocked = {(5, 4)}

        result = move_position(position, "right", width=8, height=8, blocked=blocked)

        self.assertEqual(result, (4, 4))

    def test_move_position_stops_at_blocked_tile(self):
        position = (3, 4)
        blocked = {(4, 4)}

        result = move_position(position, "right", width=8, height=8, blocked=blocked)

        self.assertEqual(result, (3, 4))

    def test_move_position_stops_at_map_edge(self):
        result = move_position((0, 0), "left", width=8, height=8, blocked=set())

        self.assertEqual(result, (0, 0))

    def test_find_event_returns_matching_event_name(self):
        events = {
            (5, 5): "well",
            (8, 2): "mayor",
        }

        self.assertEqual(find_event((8, 2), events), "mayor")
        self.assertIsNone(find_event((1, 1), events))

    def test_tile_to_pixels_respects_tile_size_and_offset(self):
        result = tile_to_pixels((2, 3), tile_size=64, offset=(32, 16))

        self.assertEqual(result, (160, 208))

    def test_all_live_maps_are_valid(self):
        for map_data in EXPLORATION_MAPS.values():
            self.assertEqual(validate_map_data(map_data), [])

    def test_all_live_maps_have_reachable_main_event(self):
        for map_data in EXPLORATION_MAPS.values():
            main_event = map_data["main_event"]
            main_tile = next(
                tile_position
                for tile_position, event_name in map_data["events"].items()
                if event_name == main_event
            )

            path_length = shortest_path_length(
                map_data["start"],
                main_tile,
                width=map_data["width"],
                height=map_data["height"],
                blocked=map_data["blocked"],
            )

            self.assertIsNotNone(path_length)
            self.assertGreater(path_length, 0)

    def test_anozira_square_main_objective_routes_to_market_meeting(self):
        map_data = EXPLORATION_MAPS["anozira_square"]

        self.assertEqual(map_data["main_event"], "market_exit")
        self.assertIn("embrum", map_data["objective"].lower())
        self.assertEqual(map_data["events"][(19, 6)], "market_exit")
        self.assertEqual(map_data["event_markers"]["market_exit"], "TALK")
        self.assertEqual(map_data["event_short_labels"]["market_exit"], "Embrum")

    def test_anozira_square_uses_static_marker_selection_layout(self):
        map_data = EXPLORATION_MAPS["anozira_square"]

        self.assertEqual(map_data["mode"], "marker_select")
        self.assertEqual(
            set(map_data["marker_positions"].keys()),
            {"well", "villager", "market_exit"},
        )

    def test_all_live_maps_have_edge_exit_markers(self):
        for map_data in EXPLORATION_MAPS.values():
            edge_event = map_data["edge_exit_event"]

            edge_tiles = [
                tile_position
                for tile_position, event_name in map_data["events"].items()
                if event_name == edge_event
            ]

            self.assertTrue(edge_tiles)

            for tile_x, tile_y in edge_tiles:
                self.assertTrue(
                    tile_x in {0, map_data["width"] - 1}
                    or tile_y in {0, map_data["height"] - 1}
                )

    def test_shortest_path_returns_walkable_route(self):
        blocked = {(1, 0), (1, 1)}

        path = shortest_path(
            (0, 0),
            (2, 0),
            width=4,
            height=4,
            blocked=blocked,
        )

        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (2, 0))
        self.assertNotIn((1, 0), path)
        self.assertNotIn((1, 1), path)
        self.assertGreater(len(path), 3)

    def test_format_quest_log_entry_avoids_renpy_bracket_interpolation(self):
        entry = format_quest_log_entry("MAIN", "Meet Embrum and Mayor Vale")

        self.assertEqual(entry, "MAIN: Meet Embrum and Mayor Vale")
        self.assertNotIn("[", entry)
        self.assertNotIn("]", entry)

    def test_marker_anchor_pulls_edge_markers_inward(self):
        self.assertEqual(marker_anchor((19, 6), width=20, height=11), (1.0, 0.0))
        self.assertEqual(marker_anchor((0, 6), width=20, height=11), (0.0, 0.0))
        self.assertEqual(marker_anchor((8, 10), width=20, height=11), (0.0, 1.0))

if __name__ == "__main__":
    unittest.main()
