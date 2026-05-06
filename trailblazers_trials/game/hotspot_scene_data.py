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
                "marker": "WELL",
                "short_label": "Well",
                "title": "Inspect the village well",
                "x": 805,
                "y": 360,
                "target": "well",
            },
            {
                "id": "villager",
                "marker": "TALK",
                "short_label": "Villager",
                "title": "Talk to the local villager",
                "x": 1120,
                "y": 600,
                "target": "villager",
            },
            {
                "id": "market_day",
                "marker": "TALK",
                "short_label": "Market",
                "title": "Visit the market while it is still open",
                "x": 315,
                "y": 675,
                "target": "market_day",
            },
            {
                "id": "tavern",
                "marker": "TALK",
                "short_label": "Tavern",
                "title": "Enter the tavern for a crucial lead",
                "x": 420,
                "y": 655,
                "target": "tavern",
                "requires": ["tavern_unlocked"],
            },
            {
                "id": "mine_path",
                "marker": "GO",
                "short_label": "Mine Path",
                "title": "Head toward the mine path",
                "x": 1320,
                "y": 250,
                "target": "mine_path",
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
                "marker": "TALK",
                "short_label": "Father",
                "title": "Speak with the drunk father",
                "x": 355,
                "y": 505,
                "target": "drunk_father",
            },
            {
                "id": "wounded_miner",
                "marker": "TALK",
                "short_label": "Miner",
                "title": "Check on the wounded miner",
                "x": 900,
                "y": 460,
                "target": "wounded_miner",
            },
            {
                "id": "leave_tavern",
                "marker": "EXIT",
                "short_label": "Leave",
                "title": "Leave the tavern",
                "x": 1270,
                "y": 210,
                "target": "leave_tavern",
                "requires": ["heard_dead_miner_hint"],
            },
        ],
    },
}
