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
        "guarding": False,
    }


def _party_states(encounter):
    party_data = encounter.get("party") or [encounter["player"]]
    return [
        _actor_state(actor_data, slot_index)
        for slot_index, actor_data in enumerate(party_data)
    ]


def active_actor(state):
    active_actor_id = state.get("active_actor_id")
    for actor in state["party"]:
        if actor["id"] == active_actor_id:
            return actor
    return state["party"][0]


def start_battle(encounter):
    party = _party_states(encounter)
    active_actor_id = encounter.get("active_actor_id", party[0]["id"])
    active = next(
        (actor for actor in party if actor["id"] == active_actor_id),
        party[0],
    )

    return {
        "title": encounter["title"],
        "summary": encounter["summary"],
        "background": encounter.get("background", "bg severance dark"),
        "party": party,
        "active_actor_id": active["id"],
        "player": active,
        "enemy": _actor_state(encounter["enemy"]),
        "actions": encounter["actions"],
        "player_actions": list(active["actions"]),
        "enemy_attack": encounter["enemy"]["attack"],
        "enemy_attack_cost": encounter["enemy"].get("attack_cost", 1),
        "turn": "player",
        "outcome": None,
        "log": ["Oren enters the quiet training space."],
    }


def _damage_actor(actor, damage):
    actor["hp"] = max(0, actor["hp"] - damage)


def _restore_actor_ap(actor, amount):
    actor["ap"] = min(actor["max_ap"], actor["ap"] + amount)


def _enemy_counterattack(state):
    active = active_actor(state)
    cost = state.get("enemy_attack_cost", 1)
    if state["enemy"].get("ap", 0) < cost:
        _restore_actor_ap(state["enemy"], 2)
        state["log"].append("The training shade gathers its rhythm.")
        return

    state["enemy"]["ap"] -= cost
    damage = state["enemy_attack"]
    if active.get("guarding"):
        damage = max(1, damage // 2)

    _damage_actor(active, damage)
    active["guarding"] = False

    state["log"].append(
        "The training shade answers for %d damage." % damage
    )

    if all(actor["hp"] <= 0 for actor in state["party"]):
        state["outcome"] = "defeat"


def resolve_player_action(state, action_id):
    if state.get("outcome"):
        return state

    active = active_actor(state)

    if action_id not in state["actions"]:
        state["log"].append("%s cannot use that action." % active["name"])
        return state

    action = state["actions"][action_id]
    cost = action.get("cost", 0)
    if active.get("ap", 0) < cost:
        state["log"].append("%s needs %d AP, but has not enough AP." % (
            active["name"],
            cost,
        ))
        return state

    active["ap"] -= cost
    state["log"].append(action["message"])

    if action.get("guard"):
        active["guarding"] = True

    damage = action.get("damage", 0)
    if damage:
        _damage_actor(state["enemy"], damage)

    restores_ap = action.get("restores_ap", 0)
    if restores_ap:
        _restore_actor_ap(active, restores_ap)

    if state["enemy"]["hp"] <= 0:
        state["outcome"] = "victory"
        state["log"].append("The training shade breaks apart into quiet sparks.")
        return state

    _enemy_counterattack(state)
    state["turn"] = "player"
    return state
