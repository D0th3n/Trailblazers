EXPLORATION_TILE_SIZE = 64
EXPLORATION_MAP_ORIGIN = (0, 0)


TREE_BLOCKS = {
    (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
    (15, 0), (16, 0), (17, 0), (18, 0), (19, 0),
    (0, 1), (19, 1),
    (0, 2), (19, 2),
    (0, 9), (19, 9),
    (0, 10), (1, 10), (18, 10), (19, 10),
}


HOUSE_BLOCKS = {
    (2, 2), (3, 2), (4, 2),
    (2, 3), (3, 3), (4, 3),
    (2, 4), (3, 4), (4, 4),
    (15, 1), (16, 1), (17, 1),
    (15, 2), (16, 2), (17, 2),
    (15, 3), (16, 3), (17, 3),
}


FENCE_BLOCKS = {
    (6, 4), (7, 4), (8, 4),
    (6, 5), (8, 5),
    (6, 6), (7, 6), (8, 6),
}


PROP_BLOCKS = {
    (10, 5),
    (14, 5),
    (16, 5), (17, 5),
    (5, 7),
}


EXPLORATION_MAPS = {
    "anozira_square": {
        "mode": "marker_select",
        "background": "bg anozira exploration",
        "width": 20,
        "height": 11,
        "tile_size": EXPLORATION_TILE_SIZE,
        "origin": EXPLORATION_MAP_ORIGIN,
        "start": (2, 8),
        "blocked": TREE_BLOCKS | HOUSE_BLOCKS | FENCE_BLOCKS | PROP_BLOCKS,
        "events": {
            (10, 5): "well",
            (4, 7): "villager",
            (19, 6): "market_exit",
        },
        "event_walk_to": {
            "well": (10, 6),
        },
        "main_event": "market_exit",
        "edge_exit_event": "market_exit",
        "quest_order": ["market_exit", "villager", "well"],
        "marker_positions": {
            "market_exit": (315, 675),
            "villager": (1120, 600),
            "well": (800, 385),
        },
        "event_markers": {
            "well": "WELL",
            "villager": "TALK",
            "market_exit": "TALK",
        },
        "event_short_labels": {
            "well": "Well",
            "villager": "Villager",
            "market_exit": "Embrum",
        },
        "event_titles": {
            "well": "Inspect the steaming well",
            "villager": "Talk to the frightened villager",
            "market_exit": "Talk to Embrum at the village market",
        },
        "event_descriptions": {
            "well": "Check the village well for signs of the drought.",
            "villager": "Ask a local what they have seen near the hot ground.",
            "market_exit": "Click to continue the story by talking to Embrum at the market stalls.",
        },
        "completion_flags": {
            "well": "explored_village_well",
            "villager": "explored_village_rumor",
        },
        "objective": "Choose where Oren investigates, then meet Embrum at the market.",
    },
    "ruzen_mine_approach_walk": {
        "background": "bg ruzen mine entrance",
        "width": 16,
        "height": 9,
        "tile_size": EXPLORATION_TILE_SIZE,
        "origin": EXPLORATION_MAP_ORIGIN,
        "start": (2, 7),
        "blocked": {
            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
            (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0),
            (0, 1), (15, 1),
            (0, 2), (15, 2),
            (0, 3), (15, 3),
            (0, 4), (15, 4),
            (0, 5), (15, 5),
            (0, 6), (15, 6),
            (0, 7), (15, 7),
            (0, 8), (1, 8), (14, 8), (15, 8),
            (8, 3), (9, 3), (10, 3),
            (11, 5), (12, 5),
        },
        "events": {
            (4, 6): "foreman",
            (8, 4): "sealed_gate",
            (12, 6): "supply_cart",
            (8, 0): "mine_exit",
        },
        "event_walk_to": {
            "sealed_gate": (8, 5),
            "mine_exit": (8, 1),
        },
        "main_event": "foreman",
        "edge_exit_event": "mine_exit",
        "quest_order": ["foreman", "sealed_gate", "supply_cart"],
        "event_markers": {
            "foreman": "GO",
            "sealed_gate": "GATE",
            "supply_cart": "CART",
            "mine_exit": "EXIT",
        },
        "event_short_labels": {
            "foreman": "Foreman",
            "sealed_gate": "Gate",
            "supply_cart": "Cart",
            "mine_exit": "Tunnel",
        },
        "event_titles": {
            "foreman": "Talk to the mine foreman",
            "sealed_gate": "Inspect the sealed mine gate",
            "supply_cart": "Inspect the abandoned supply cart",
            "mine_exit": "Descend into the deeper mine tunnels",
        },
        "event_descriptions": {
            "foreman": "Main route into the future Ruzen mine exploration sequence.",
            "sealed_gate": "A clue point for the unstable lower entrance.",
            "supply_cart": "A prop interaction point near the mine approach.",
            "mine_exit": "Edge transition marker for continuing deeper into the mine route.",
        },
        "completion_flags": {},
        "objective": "Prepared for future mine exploration: start with the foreman at the GO marker.",
    }
}
