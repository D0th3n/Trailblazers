ROMAN_TIERS = {
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "V",
}


def tier_label(base_label, tier):
    roman = ROMAN_TIERS.get(tier, str(tier))
    return "%s %s" % (base_label, roman)


def tiered_spell(base_label, tier=1, tiers=None, **action):
    tiers = tiers or {}
    action = dict(action)
    action["base_label"] = base_label
    action["tier"] = tier
    action["tiers"] = tiers
    action["label"] = tier_label(base_label, tier)
    if tier in tiers:
        action.update(tiers[tier])
    return action


SPELL_TIER_TRACKS = {
    "fire_ball": {
        1: {"cost": 2, "qana_cost": 3, "damage": 4, "tick_damage": 2},
        2: {"cost": 3, "qana_cost": 4, "damage": 6, "tick_damage": 3},
        3: {"cost": 4, "qana_cost": 5, "damage": 8, "tick_damage": 4, "splash_damage": 2},
    },
    "healing_burst": {
        1: {"cost": 2, "qana_cost": 3, "heals_hp": 5},
        2: {"cost": 3, "qana_cost": 4, "heals_hp": 8},
        3: {"cost": 4, "qana_cost": 5, "heals_hp": 11, "restores_stamina": 1},
    },
    "freeze_ray": {
        1: {"cost": 3, "qana_cost": 4, "damage": 3, "freeze_rounds": 2},
        2: {"cost": 4, "qana_cost": 5, "damage": 5, "freeze_rounds": 2},
        3: {"cost": 5, "qana_cost": 6, "damage": 7, "freeze_rounds": 3},
    },
    "dragon_geisure": {
        1: {"cost": 5, "qana_cost": 6, "damage": 6, "tick_damage": 3, "chaos_gain": 5},
        2: {"cost": 6, "qana_cost": 7, "damage": 9, "tick_damage": 4, "chaos_gain": 6},
        3: {"cost": 7, "qana_cost": 8, "damage": 12, "tick_damage": 5, "chaos_gain": 7},
    },
    "dragon_javelin": {
        1: {"cost": 5, "qana_cost": 5, "damage": 8, "pierce_chance": 0.2, "chaos_gain": 4},
        2: {"cost": 6, "qana_cost": 6, "damage": 11, "pierce_chance": 0.35, "chaos_gain": 5},
        3: {"cost": 7, "qana_cost": 7, "damage": 14, "pierce_chance": 0.5, "chaos_gain": 6},
    },
}


OREN_STARTING_SKILL_TIERS = {
    "fire_ball": 1,
    "healing_burst": 1,
    "freeze_ray": 1,
    "dragon_geisure": 1,
    "dragon_javelin": 1,
}


OREN_ACTIONS = {
    "attack": {
        "label": "Basic Attack",
        "category": "Attack",
        "cost": 2,
        "uses_per_round": 5,
        "damage": 6,
        "message": "Oren strikes the training shade with a clean practice cut.",
    },
    "guard": {
        "label": "Block",
        "category": "Defense",
        "cost": 0,
        "stamina_cost": 2,
        "damage": 0,
        "guard": True,
        "message": "Oren lowers his stance and braces for the counter.",
    },
    "dodge": {
        "label": "Dodge",
        "category": "Defense",
        "cost": 0,
        "stamina_cost": 2,
        "dodge_chance": 0.667,
        "heals_on_dodge": 1,
        "message": "Oren shifts his weight, ready to dodge the next attack.",
    },
    "ember_focus": {
        "label": "Ultimate",
        "category": "Ultimate",
        "cost": 5,
        "uses_per_round": 1,
        "damage": 10,
        "message": "Oren draws a thin ember of resolve through the imagined blade.",
    },
    "focus": {
        "label": "AP Recovery",
        "category": "AP Recovery",
        "cost": 0,
        "uses_per_round": 1,
        "restores_ap": 3,
        "damage": 0,
        "message": "Oren steadies his breathing and gathers his rhythm again.",
    },
    "fire_ball": tiered_spell(
        "Fire Ball",
        tier=1,
        tiers=SPELL_TIER_TRACKS["fire_ball"],
        **{
            "category": "Qana",
            "uses_per_round": 2,
            "tick_rounds": 3,
            "message": "Oren casts Fire Ball, bursting flame across the target.",
        },
    ),
    "healing_burst": tiered_spell(
        "Healing Burst",
        tier=1,
        tiers=SPELL_TIER_TRACKS["healing_burst"],
        **{
            "category": "Qana",
            "uses_per_round": 2,
            "message": "Oren releases a warm burst of Qana and closes his wounds.",
        },
    ),
    "freeze_ray": tiered_spell(
        "Freeze Ray",
        tier=1,
        tiers=SPELL_TIER_TRACKS["freeze_ray"],
        **{
            "category": "Qana",
            "uses_per_round": 1,
            "message": "Oren sends out a beam of cold Qana.",
        },
    ),
    "dragon_geisure": tiered_spell(
        "Dragon Geisure",
        tier=1,
        tiers=SPELL_TIER_TRACKS["dragon_geisure"],
        **{
            "category": "Dragon Spells",
            "requires_dragon_spells": True,
            "uses_per_round": 1,
            "tick_rounds": 3,
            "max_targets": 5,
            "message": "Dragon flames geyser out of the ground beneath the enemy line.",
        },
    ),
    "dragon_javelin": tiered_spell(
        "Dragon Javelin",
        tier=1,
        tiers=SPELL_TIER_TRACKS["dragon_javelin"],
        **{
            "category": "Dragon Spells",
            "requires_dragon_spells": True,
            "uses_per_round": 1,
            "message": "Oren hurls a Dragon Javelin through the target.",
        },
    ),
    "health_elixir": {
        "label": "Health Elixir",
        "category": "Items",
        "cost": 0,
        "heals_hp": 3,
        "starting_uses": 1,
        "use_capacity": 2,
        "message": "Oren drinks a Health Elixir and regains a little strength.",
    },
    "qana_elixir": {
        "label": "Qana Elixir",
        "category": "Items",
        "cost": 0,
        "restores_qana": 3,
        "starting_uses": 1,
        "use_capacity": 2,
        "message": "Oren drinks a Qana Elixir and recovers inner force.",
    },
}


OREN_PARTY_MEMBER = {
    "id": "oren",
    "name": "Oren",
    "sprite": "combat oren idle",
    "max_hp": 30,
    "max_ap": 5,
    "max_qana": 10,
    "max_stamina": 6,
    "max_chaos": 10,
    "allow_dragon_spells": True,
    "skill_tiers": dict(OREN_STARTING_SKILL_TIERS),
    "actions": [
        "attack",
        "guard",
        "dodge",
        "ember_focus",
        "focus",
        "fire_ball",
        "healing_burst",
        "freeze_ray",
        "dragon_geisure",
        "dragon_javelin",
        "health_elixir",
        "qana_elixir",
    ],
}


BATTLE_ENCOUNTERS = {
    "meditation_dummy": {
        "title": "Meditation Training",
        "summary": "A mental sparring form built from Oren's own doubts.",
        "background": "bg severance dark",
        "active_actor_id": "oren",
        "party": [
            OREN_PARTY_MEMBER,
        ],
        "enemy": {
            "id": "training_shade",
            "name": "Training Shade",
            "sprite": "combat training dummy temp idle",
            "max_hp": 20,
            "max_ap": 5,
            "max_qana": 8,
            "max_stamina": 4,
            "max_chaos": 0,
            "attack": 4,
            "attack_cost": 1,
            "actions": ["freeze_ray"],
            "freeze_ray_damage": 4,
        },
        "actions": OREN_ACTIONS,
    },
    "team_dummy": {
        "title": "Team Meditation Training",
        "summary": "A paired battle exercise with allied and enemy training dummies.",
        "background": "bg severance dark",
        "active_actor_id": "oren",
        "controlled_party_turns": True,
        "party": [
            OREN_PARTY_MEMBER,
            {
                "id": "ally_dummy",
                "name": "Ally Dummy",
                "sprite": "combat ally dummy temp idle",
                "max_hp": 28,
                "max_ap": 5,
                "max_qana": 10,
                "max_stamina": 6,
                "max_chaos": 10,
                "attack": 5,
                "actions": list(OREN_PARTY_MEMBER["actions"]),
            },
        ],
        "enemies": [
            {
                "id": "training_shade",
                "name": "Enemy Dummy",
                "sprite": "combat training dummy temp idle",
                "max_hp": 20,
                "max_ap": 5,
                "max_qana": 8,
                "max_stamina": 4,
                "max_chaos": 0,
                "attack": 4,
                "attack_cost": 1,
                "actions": ["freeze_ray"],
                "freeze_ray_damage": 4,
            },
            {
                "id": "support_shade",
                "name": "Enemy Support Dummy",
                "sprite": "combat training dummy temp idle",
                "max_hp": 16,
                "max_ap": 4,
                "max_qana": 4,
                "max_stamina": 4,
                "max_chaos": 0,
                "attack": 2,
                "attack_cost": 1,
                "actions": [],
            },
        ],
        "actions": OREN_ACTIONS,
    },
}
