BATTLE_ENCOUNTERS = {
    "meditation_dummy": {
        "title": "Meditation Training",
        "summary": "A mental sparring form built from Oren's own doubts.",
        "background": "bg severance dark",
        "active_actor_id": "oren",
        "party": [
            {
                "id": "oren",
                "name": "Oren",
                "sprite": "combat oren temp idle",
                "max_hp": 30,
                "max_ap": 5,
                "actions": ["attack", "guard", "ember_focus", "focus"],
            },
        ],
        "enemy": {
            "id": "training_shade",
            "name": "Training Shade",
            "sprite": "combat training dummy temp idle",
            "max_hp": 20,
            "max_ap": 5,
            "attack": 4,
            "attack_cost": 1,
        },
        "actions": {
            "attack": {
                "label": "Attack",
                "category": "Attack",
                "cost": 1,
                "damage": 6,
                "message": "Oren strikes the training shade with a clean practice cut.",
            },
            "guard": {
                "label": "Guard",
                "category": "Defense",
                "cost": 1,
                "damage": 0,
                "guard": True,
                "message": "Oren lowers his stance and braces for the counter.",
            },
            "ember_focus": {
                "label": "Ember Focus",
                "category": "Feats",
                "cost": 2,
                "damage": 10,
                "message": "Oren draws a thin ember of resolve through the imagined blade.",
            },
            "focus": {
                "label": "Focus",
                "category": "Support",
                "cost": 0,
                "restores_ap": 3,
                "damage": 0,
                "message": "Oren steadies his breathing and gathers his rhythm again.",
            },
        },
    },
}
