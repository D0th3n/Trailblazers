def _completed_set(completed_actions):
    return set(completed_actions or [])


def hotspot_state(scene_data, hotspot_id, completed_actions=None):
    hotspot = scene_data["hotspots"][hotspot_id]
    completed = _completed_set(completed_actions)

    completed_by = hotspot.get("completes")
    if completed_by and completed_by in completed and hotspot.get("hide_when_complete", False):
        return {
            "enabled": False,
            "hidden": True,
            "message": None,
        }

    missing = [
        action
        for action in hotspot.get("requires", [])
        if action not in completed
    ]

    return {
        "enabled": not missing,
        "hidden": False,
        "message": hotspot.get("blocked_message") if missing else None,
    }


def visible_hotspot_ids(scene_data, completed_actions=None):
    visible = []
    for hotspot_id in scene_data.get("hotspot_order", scene_data["hotspots"].keys()):
        state = hotspot_state(scene_data, hotspot_id, completed_actions)
        if not state["hidden"]:
            visible.append(hotspot_id)
    return visible


def scene_complete(scene_data, completed_actions=None):
    completed = _completed_set(completed_actions)
    return all(
        action in completed
        for action in scene_data.get("required_actions", [])
    )
