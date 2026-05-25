INTERACTIVE_SCENES = {
    "chapter_02_room": {
        "title": "Oren's Room",
        "objective": "Get dressed before leaving the room.",
        "required_actions": ["get_dressed"],
        "hotspot_order": ["dresser", "meditation", "door"],
        "hotspots": {
            "dresser": {
                "label": "Armor Stand",
                "icon": "!",
                "xpos": 0.63,
                "ypos": 0.55,
                "completes": "get_dressed",
                "hide_when_complete": True,
                "description": "Put on Oren's armor.",
            },
            "meditation": {
                "label": "Meditation",
                "icon": "*",
                "xpos": 0.45,
                "ypos": 0.68,
                "description": "Train inside Oren's mind.",
            },
            "door": {
                "label": "Door",
                "icon": "->",
                "xpos": 0.88,
                "ypos": 0.43,
                "requires": ["get_dressed"],
                "blocked_message": "I should get dressed before I leave.",
                "description": "Step into the inn hallway.",
            },
        },
    },
}
