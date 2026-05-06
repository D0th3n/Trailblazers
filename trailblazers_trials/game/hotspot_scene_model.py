from hotspot_scene_data import SCREEN_H, SCREEN_W


def _flag_is_enabled(flags, flag_name):
    if hasattr(flags, "get"):
        return bool(flags.get(flag_name, False))

    return bool(flag_name in flags)


def available_hotspots(scene, flags):
    hotspots = scene.get("hotspots", [])
    visible_hotspots = []

    for hotspot in hotspots:
        required_flags = hotspot.get("requires", [])
        if all(_flag_is_enabled(flags, flag) for flag in required_flags):
            visible_hotspots.append(hotspot)

    return visible_hotspots


def validate_hotspot_scene(scene):
    problems = []

    if not scene.get("background"):
        problems.append("missing_background")

    hotspots = scene.get("hotspots", [])
    if not hotspots:
        problems.append("missing_hotspots")

    for hotspot in hotspots:
        hotspot_id = hotspot.get("id", "unknown")
        x = hotspot.get("x")
        y = hotspot.get("y")

        if x is None or y is None or x < 0 or x >= SCREEN_W or y < 0 or y >= SCREEN_H:
            problems.append("hotspot_out_of_bounds:%s" % hotspot_id)

    return problems


def validate_hotspot_registry(registry):
    problems = []

    for scene_id, scene in registry.items():
        for problem in validate_hotspot_scene(scene):
            problems.append("%s:%s" % (scene_id, problem))

    return problems
