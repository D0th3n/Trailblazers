SCREEN_W = 1600
SCREEN_H = 900


HOTSPOT_SCENE_REGISTRY = {
    "anozira_overview": {
        "scene_id": "anozira_overview",
        "background": "bg anozira exploration",
        "title": "Anozira Village Investigation",
        "objective": (
            "Choose where Oren investigates during the day. The tavern is "
            "mandatory before the mine opens at dawn."
        ),
        "hotspots": [
            {
                "id": "well",
                "label": "Well",
                "x": 805,
                "y": 360,
            },
            {
                "id": "villager",
                "label": "Villager",
                "x": 1120,
                "y": 600,
            },
            {
                "id": "market_day",
                "label": "Market Day",
                "x": 315,
                "y": 675,
            },
            {
                "id": "tavern",
                "label": "Tavern",
                "x": 420,
                "y": 655,
                "requires": ["tavern_unlocked"],
            },
            {
                "id": "mine_path",
                "label": "Mine Path",
                "x": 1320,
                "y": 250,
                "requires": ["mine_unlocked"],
            },
        ],
    },
    "tavern_room": {
        "scene_id": "tavern_room",
        "background": "bg tavern night",
        "title": "Anozira Tavern",
        "objective": (
            "Choose who Oren speaks to first before the mine briefing ends for "
            "the night."
        ),
        "hotspots": [
            {
                "id": "drunk_father",
                "label": "Drunk Father",
                "x": 355,
                "y": 505,
            },
            {
                "id": "wounded_miner",
                "label": "Wounded Miner",
                "x": 900,
                "y": 460,
            },
            {
                "id": "leave_tavern",
                "label": "Leave Tavern",
                "x": 1270,
                "y": 210,
                "requires": ["heard_dead_miner_hint"],
            },
        ],
    },
}
