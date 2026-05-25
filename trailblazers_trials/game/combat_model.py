import random


def _actor_state(actor_data, slot_index=0):
    return {
        "id": actor_data["id"],
        "name": actor_data["name"],
        "sprite": actor_data.get("sprite"),
        "actions": list(actor_data.get("actions", [])),
        "slot_index": slot_index,
        "max_hp": actor_data["max_hp"],
        "hp": actor_data["max_hp"],
        "max_ap": actor_data.get("max_ap", 0),
        "ap": actor_data.get("max_ap", 0),
        "max_qana": actor_data.get("max_qana", 0),
        "qana": actor_data.get("max_qana", 0),
        "max_stamina": actor_data.get("max_stamina", 0),
        "stamina": actor_data.get("max_stamina", 0),
        "max_chaos": actor_data.get("max_chaos", 0),
        "chaos": 0,
        "attack": actor_data.get("attack", 0),
        "attack_cost": actor_data.get("attack_cost", 1),
        "freeze_ray_damage": actor_data.get("freeze_ray_damage"),
        "allow_dragon_spells": actor_data.get("allow_dragon_spells", False),
        "skill_tiers": dict(actor_data.get("skill_tiers", {})),
        "guarding": False,
        "dodging": False,
        "status_effects": [],
        "skip_counterattacks": 0,
    }


def _party_states(encounter):
    party_data = encounter.get("party") or [encounter["player"]]
    return [_actor_state(actor_data, slot_index) for slot_index, actor_data in enumerate(party_data)]


def _enemy_states(encounter):
    enemy_data = encounter.get("enemies") or [encounter["enemy"]]
    return [_actor_state(actor_data, slot_index) for slot_index, actor_data in enumerate(enemy_data)]


def active_actor(state):
    active_actor_id = state.get("active_actor_id")
    for actor in state["party"]:
        if actor["id"] == active_actor_id:
            return actor
    return state["party"][0]


def _set_active_actor(state, actor_id):
    state["active_actor_id"] = actor_id
    state["player"] = active_actor(state)
    state["player_actions"] = list(state["player"].get("actions", []))


def alive_party(state):
    return [actor for actor in state["party"] if actor["hp"] > 0]


def alive_enemies(state):
    return [actor for actor in state["enemies"] if actor["hp"] > 0]


def primary_enemy(state):
    enemies = alive_enemies(state)
    if enemies:
        return enemies[0]
    return state["enemies"][0]


ROMAN_TIERS = {
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "V",
}


def tier_label(base_label, tier):
    return "%s %s" % (base_label, ROMAN_TIERS.get(tier, str(tier)))


def action_for_actor(state, actor, action_id):
    action = dict(state["actions"].get(action_id, {}))
    tiers = action.get("tiers", {})
    if tiers:
        tier = actor.get("skill_tiers", {}).get(action_id, action.get("tier", 1))
        tier = max(1, min(tier, max(tiers.keys())))
        action.update(tiers.get(tier, {}))
        action["tier"] = tier
        action["label"] = tier_label(action.get("base_label", action["label"]), tier)
    return action


def set_actor_skill_tier(state, actor_id, action_id, tier):
    for actor in state["party"] + state["enemies"]:
        if actor["id"] == actor_id:
            actor.setdefault("skill_tiers", {})[action_id] = tier
            return state
    return state


def start_battle(encounter, inventory=None):
    party = _party_states(encounter)
    enemies = _enemy_states(encounter)
    active_actor_id = encounter.get("active_actor_id", party[0]["id"])
    active = next((actor for actor in party if actor["id"] == active_actor_id), party[0])
    for actor in party:
        actor["team"] = "party"
    for actor in enemies:
        actor["team"] = "enemy"
    return {
        "title": encounter["title"],
        "summary": encounter["summary"],
        "background": encounter.get("background", "bg severance dark"),
        "party": party,
        "enemies": enemies,
        "active_actor_id": active["id"],
        "player": active,
        "enemy": enemies[0],
        "turn_order": party + enemies,
        "actions": encounter["actions"],
        "player_actions": list(active["actions"]),
        "enemy_attack": enemies[0]["attack"],
        "enemy_attack_cost": enemies[0].get("attack_cost", 1),
        "turn": "player",
        "round": 1,
        "actions_taken": 0,
        "controlled_party_turns": encounter.get("controlled_party_turns", False),
        "acted_actor_ids": [],
        "pending_round_start": False,
        "round_action_uses": {},
        "battle_action_uses": {},
        "inventory_counts": dict(inventory or {}),
        "last_action": None,
        "outcome": None,
        "log": ["Battle Start", "Click Oren to choose an action."],
    }


def _damage_actor(actor, damage):
    actor["hp"] = max(0, actor["hp"] - damage)


def _restore_actor_ap(actor, amount):
    actor["ap"] = min(actor["max_ap"], actor["ap"] + amount)


def _restore_actor_hp(actor, amount):
    actor["hp"] = min(actor["max_hp"], actor["hp"] + amount)


def _restore_actor_qana(actor, amount):
    actor["qana"] = min(actor.get("max_qana", 0), actor.get("qana", 0) + amount)


def _restore_actor_stamina(actor, amount):
    actor["stamina"] = min(actor.get("max_stamina", 0), actor.get("stamina", 0) + amount)


def _record_feedback(state, actor, target, action_id, action_label, damage, kind):
    state["last_action"] = {
        "actor_id": actor["id"],
        "actor_name": actor["name"],
        "actor_team": actor.get("team", ""),
        "target_id": target["id"] if target else None,
        "target_name": target["name"] if target else "",
        "target_team": target.get("team", "") if target else "",
        "action_id": action_id,
        "action_label": action_label,
        "damage": damage,
        "kind": kind,
    }


def action_round_limit(state, action_id):
    action = action_for_actor(state, active_actor(state), action_id)
    return action.get("uses_per_round")


def action_use_capacity(state, action_id):
    action = action_for_actor(state, active_actor(state), action_id)
    round_limit = action.get("uses_per_round")
    if round_limit is not None:
        return round_limit
    return action.get("use_capacity")


def _round_use_key(state, action_id):
    return "%s:%s" % (active_actor(state)["id"], action_id)


def _actor_can_access_action(actor, action):
    if action.get("requires_dragon_spells"):
        return actor.get("allow_dragon_spells", False)
    return True


def action_uses_remaining(state, action_id):
    action = action_for_actor(state, active_actor(state), action_id)
    round_limit = action.get("uses_per_round")
    if round_limit is not None:
        used = state.get("round_action_uses", {}).get(_round_use_key(state, action_id), 0)
        return max(0, round_limit - used)
    use_capacity = action.get("use_capacity")
    if use_capacity is None:
        return None
    if "inventory_counts" in state:
        return min(use_capacity, state["inventory_counts"].get(action_id, 0))
    starting_uses = action.get("starting_uses", use_capacity)
    used = state.get("battle_action_uses", {}).get(action_id, 0)
    return max(0, starting_uses - used)


def action_can_be_used(state, action_id):
    active = active_actor(state)
    if state.get("pending_round_start"):
        return False
    if action_id not in state["actions"] or action_id not in active.get("actions", []):
        return False
    action = action_for_actor(state, active, action_id)
    if not _actor_can_access_action(active, action):
        return False
    remaining = action_uses_remaining(state, action_id)
    if remaining == 0:
        return False
    if active.get("ap", 0) < action.get("cost", 0):
        return False
    if active.get("qana", 0) < action.get("qana_cost", 0):
        return False
    if active.get("stamina", 0) < action.get("stamina_cost", 0):
        return False
    return True


def _record_action_use(state, action_id):
    if action_round_limit(state, action_id) is None:
        action = action_for_actor(state, active_actor(state), action_id)
        if action.get("use_capacity") is None:
            return
        if "inventory_counts" in state:
            state["inventory_counts"][action_id] = max(0, state["inventory_counts"].get(action_id, 0) - 1)
            return
        state.setdefault("battle_action_uses", {})
        state["battle_action_uses"][action_id] = state["battle_action_uses"].get(action_id, 0) + 1
        return
    state.setdefault("round_action_uses", {})
    use_key = _round_use_key(state, action_id)
    state["round_action_uses"][use_key] = state["round_action_uses"].get(use_key, 0) + 1


def _apply_round_status_effects(state):
    for enemy in state["enemies"]:
        remaining_effects = []
        for effect in enemy.get("status_effects", []):
            if effect.get("type") == "burn":
                damage = effect.get("damage", 0)
                if damage:
                    _damage_actor(enemy, damage)
                    state["log"].append("%s takes %d lingering fire damage." % (enemy["name"], damage))
            effect["rounds"] = effect.get("rounds", 0) - 1
            if effect["rounds"] > 0:
                remaining_effects.append(effect)
        enemy["status_effects"] = remaining_effects
    if not alive_enemies(state):
        state["outcome"] = "victory"
        state["log"].append("The enemy line breaks apart into quiet sparks.")


def _begin_next_round(state):
    state["pending_round_start"] = False
    state["round"] = state.get("round", 1) + 1
    state["acted_actor_ids"] = []
    state["round_action_uses"] = {}
    for actor in state["party"]:
        actor["ap"] = actor["max_ap"]
        actor["stamina"] = actor["max_stamina"]
    for enemy in state["enemies"]:
        enemy["ap"] = enemy["max_ap"]
    state["last_action"] = None
    state["log"].append("Round %d begins." % state["round"])
    _apply_round_status_effects(state)


def begin_pending_round(state):
    if not state.get("pending_round_start") or state.get("outcome"):
        return state
    _begin_next_round(state)
    first_actor = _next_party_actor_waiting(state)
    if first_actor is not None:
        _set_active_actor(state, first_actor["id"])
    return state


def _enemy_counterattack(state):
    active = active_actor(state)
    for enemy in alive_enemies(state):
        if enemy.get("skip_counterattacks", 0) > 0:
            enemy["skip_counterattacks"] -= 1
            active["guarding"] = False
            state["log"].append("%s is frozen and cannot attack." % enemy["name"])
            continue
        if _enemy_try_action(state, enemy, active):
            if all(actor["hp"] <= 0 for actor in state["party"]):
                state["outcome"] = "defeat"
                return
            continue
        cost = enemy.get("attack_cost", state.get("enemy_attack_cost", 1))
        if enemy.get("ap", 0) < cost:
            _restore_actor_ap(enemy, 2)
            state["log"].append("%s gathers its rhythm." % enemy["name"])
            continue
        enemy["ap"] -= cost
        damage = enemy.get("attack", state["enemy_attack"])
        if active.get("dodging"):
            active["dodging"] = False
            if random.random() < active.get("dodge_chance", 0):
                _restore_actor_hp(active, active.get("heals_on_dodge", 0))
                active["guarding"] = False
                _record_feedback(state, enemy, active, "attack", "Basic Attack", 0, "dodge")
                state["log"].append("Oren dodges cleanly and recovers 1 HP.")
                continue
            state["log"].append("Oren fails to dodge the incoming attack.")
        if active.get("guarding"):
            damage = max(1, damage // 2)
        _damage_actor(active, damage)
        active["guarding"] = False
        _record_feedback(state, enemy, active, "attack", "Basic Attack", damage, "attack")
        state["log"].append("%s answers for %d damage." % (enemy["name"], damage))
        if all(actor["hp"] <= 0 for actor in state["party"]):
            state["outcome"] = "defeat"
            return


def _enemy_try_action(state, enemy, target):
    for action_id in enemy.get("actions", []):
        if action_id not in state["actions"]:
            continue
        action = action_for_actor(state, enemy, action_id)
        cost = action.get("cost", 0)
        qana_cost = action.get("qana_cost", 0)
        stamina_cost = action.get("stamina_cost", 0)
        if enemy.get("ap", 0) < cost or enemy.get("qana", 0) < qana_cost or enemy.get("stamina", 0) < stamina_cost:
            continue
        enemy["ap"] -= cost
        enemy["qana"] -= qana_cost
        enemy["stamina"] -= stamina_cost
        damage = enemy.get("%s_damage" % action_id, action.get("damage", 0))
        if target.get("guarding"):
            damage = max(1, damage // 2)
        if target.get("dodging"):
            target["dodging"] = False
            if random.random() < target.get("dodge_chance", 0):
                _restore_actor_hp(target, target.get("heals_on_dodge", 0))
                target["guarding"] = False
                _record_feedback(state, enemy, target, action_id, action["label"], 0, "dodge")
                state["log"].append("%s dodges %s's %s." % (target["name"], enemy["name"], action["label"]))
                return True
            state["log"].append("%s fails to dodge %s's %s." % (target["name"], enemy["name"], action["label"]))
        if damage:
            _damage_actor(target, damage)
        target["guarding"] = False
        _record_feedback(state, enemy, target, action_id, action["label"], damage, "cast")
        state["log"].append("%s casts %s for %d damage." % (enemy["name"], action["label"], damage))
        return True
    return False


def _next_party_actor_waiting(state):
    acted_ids = set(state.get("acted_actor_ids", []))
    for actor in alive_party(state):
        if actor["id"] not in acted_ids:
            return actor
    return None


def _finish_controlled_party_action(state):
    active = active_actor(state)
    if active["id"] not in state["acted_actor_ids"]:
        state["acted_actor_ids"].append(active["id"])
    next_actor = _next_party_actor_waiting(state)
    if next_actor is not None:
        _set_active_actor(state, next_actor["id"])
        state["log"].append("%s is ready to act." % next_actor["name"])
        return
    _enemy_counterattack(state)
    if state.get("outcome"):
        return
    state["pending_round_start"] = True
    state["log"].append("Round %d is complete." % state.get("round", 1))


def resolve_player_action(state, action_id):
    if state.get("outcome"):
        return state
    if state.get("pending_round_start"):
        state["log"].append("Advance to the next round first.")
        return state
    active = active_actor(state)
    if action_id not in state["actions"]:
        state["log"].append("%s cannot use that action." % active["name"])
        return state
    action = action_for_actor(state, active, action_id)
    if action_id not in active.get("actions", []):
        state["log"].append("%s cannot use %s." % (active["name"], action["label"]))
        return state
    if not _actor_can_access_action(active, action):
        state["log"].append("%s cannot use Dragon Spells." % active["name"])
        return state
    remaining = action_uses_remaining(state, action_id)
    if remaining == 0:
        state["log"].append("%s has already used %s this round." % (active["name"], action["label"]))
        return state
    cost = action.get("cost", 0)
    if active.get("ap", 0) < cost:
        state["log"].append("%s needs %d AP, but has not enough AP." % (active["name"], cost))
        return state
    qana_cost = action.get("qana_cost", 0)
    if active.get("qana", 0) < qana_cost:
        state["log"].append("%s needs %d Qana, but has not enough Qana." % (active["name"], qana_cost))
        return state
    stamina_cost = action.get("stamina_cost", 0)
    if active.get("stamina", 0) < stamina_cost:
        state["log"].append("%s needs %d Stamina, but has not enough Stamina." % (active["name"], stamina_cost))
        return state
    active["ap"] -= cost
    active["qana"] -= qana_cost
    active["stamina"] -= stamina_cost
    state["actions_taken"] = state.get("actions_taken", 0) + 1
    _record_action_use(state, action_id)
    message = action["message"]
    if active["id"] != "oren":
        message = message.replace("Oren", active["name"], 1)
    state["log"].append(message)
    if action.get("guard"):
        active["guarding"] = True
    if action.get("dodge_chance"):
        active["dodging"] = True
        active["dodge_chance"] = action["dodge_chance"]
        active["heals_on_dodge"] = action.get("heals_on_dodge", 0)
    target = None
    damage = action.get("damage", 0)
    if damage:
        target = primary_enemy(state)
        _damage_actor(target, damage)
    heals_hp = action.get("heals_hp", 0)
    if heals_hp:
        _restore_actor_hp(active, heals_hp)
    restores_ap = action.get("restores_ap", 0)
    if restores_ap:
        _restore_actor_ap(active, restores_ap)
    restores_qana = action.get("restores_qana", 0)
    if restores_qana:
        _restore_actor_qana(active, restores_qana)
    restores_stamina = action.get("restores_stamina", 0)
    if restores_stamina:
        _restore_actor_stamina(active, restores_stamina)
    tick_damage = action.get("tick_damage", 0)
    tick_rounds = action.get("tick_rounds", 0)
    if tick_damage and tick_rounds:
        target = primary_enemy(state)
        target.setdefault("status_effects", []).append({"type": "burn", "damage": tick_damage, "rounds": tick_rounds})
        state["log"].append("%s will burn for %d damage over %d rounds." % (target["name"], tick_damage, tick_rounds))
    freeze_rounds = action.get("freeze_rounds", 0)
    if freeze_rounds:
        target = primary_enemy(state)
        target["skip_counterattacks"] = max(target.get("skip_counterattacks", 0), freeze_rounds)
        state["log"].append("%s is frozen for %d rounds." % (target["name"], freeze_rounds))
    pierce_chance = action.get("pierce_chance", 0)
    if pierce_chance and random.random() < pierce_chance:
        state["log"].append("Dragon Javelin did piercing damage, hitting two opponents!")
    chaos_gain = action.get("chaos_gain", 0)
    if chaos_gain:
        active["chaos"] = min(active.get("max_chaos", 0), active.get("chaos", 0) + chaos_gain)
        state["log"].append("Oren gains %d Chaos. Chaos is now %d/%d." % (chaos_gain, active["chaos"], active["max_chaos"]))
    feedback_kind = "cast" if action.get("qana_cost", 0) else "attack"
    _record_feedback(state, active, target, action_id, action["label"], damage, feedback_kind)
    if active.get("max_chaos", 0) and active.get("chaos", 0) >= active["max_chaos"]:
        active["hp"] = 0
        state["outcome"] = "defeat"
        state["log"].append("Jotunn seizes control as Chaos peaks. Oren is lost.")
        return state
    if not alive_enemies(state):
        state["outcome"] = "victory"
        state["log"].append("The enemy line breaks apart into quiet sparks.")
        return state
    if state.get("controlled_party_turns"):
        _finish_controlled_party_action(state)
        state["turn"] = "player"
        return state
    _enemy_counterattack(state)
    if not state.get("outcome") and active.get("ap", 0) <= 0:
        state["pending_round_start"] = True
        state["log"].append("Round %d is complete." % state.get("round", 1))
    state["turn"] = "player"
    return state
