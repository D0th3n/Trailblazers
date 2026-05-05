OFFSETS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}


def in_bounds(position, width, height):
    return 0 <= position[0] < width and 0 <= position[1] < height


def move_position(position, direction, width, height, blocked):
    dx, dy = OFFSETS[direction]
    next_position = (position[0] + dx, position[1] + dy)

    if not in_bounds(next_position, width, height):
        return position
    if next_position in blocked:
        return position

    return next_position


def find_event(position, events):
    return events.get(position)


def tile_to_pixels(position, tile_size, offset=(0, 0)):
    return (
        (position[0] * tile_size) + offset[0],
        (position[1] * tile_size) + offset[1],
    )


def marker_anchor(position, width, height):
    xanchor = 1.0 if position[0] >= width - 1 else 0.0
    yanchor = 1.0 if position[1] >= height - 1 else 0.0
    return xanchor, yanchor


def format_quest_log_entry(status, title):
    return "%s: %s" % (status, title)


def validate_map_data(map_data):
    problems = []
    width = map_data["width"]
    height = map_data["height"]
    start = map_data["start"]
    blocked = map_data["blocked"]
    events = map_data["events"]
    event_markers = map_data["event_markers"]
    event_titles = map_data["event_titles"]
    event_walk_to = map_data.get("event_walk_to", {})
    edge_exit_event = map_data.get("edge_exit_event")

    if not in_bounds(start, width, height):
        problems.append("start_out_of_bounds")
    if start in blocked:
        problems.append("start_blocked")

    for tile_position, event_name in events.items():
        if not in_bounds(tile_position, width, height):
            problems.append("event_out_of_bounds:%s" % event_name)
        if tile_position in blocked and event_name not in event_walk_to:
            problems.append("event_blocked:%s" % event_name)
        if event_name not in event_markers:
            problems.append("missing_marker:%s" % event_name)
        if event_name not in event_titles:
            problems.append("missing_title:%s" % event_name)
        if event_name in event_walk_to:
            walk_to = event_walk_to[event_name]
            if not in_bounds(walk_to, width, height):
                problems.append("walk_to_out_of_bounds:%s" % event_name)
            if walk_to in blocked:
                problems.append("walk_to_blocked:%s" % event_name)

    if edge_exit_event is not None:
        edge_tiles = [
            tile_position
            for tile_position, event_name in events.items()
            if event_name == edge_exit_event
        ]

        if not edge_tiles:
            problems.append("missing_edge_exit:%s" % edge_exit_event)
        else:
            for tile_x, tile_y in edge_tiles:
                on_edge = (
                    tile_x == 0
                    or tile_x == width - 1
                    or tile_y == 0
                    or tile_y == height - 1
                )
                if not on_edge:
                    problems.append("edge_exit_not_on_border:%s" % edge_exit_event)

    return problems


def shortest_path(start, goal, width, height, blocked):
    if start == goal:
        return [start]

    frontier = [start]
    parents = {start: None}

    while frontier:
        position = frontier.pop(0)

        for dx, dy in OFFSETS.values():
            next_position = (position[0] + dx, position[1] + dy)

            if next_position in parents:
                continue
            if not in_bounds(next_position, width, height):
                continue
            if next_position in blocked:
                continue

            parents[next_position] = position

            if next_position == goal:
                path = [goal]
                cursor = position
                while cursor is not None:
                    path.append(cursor)
                    cursor = parents[cursor]
                path.reverse()
                return path

            frontier.append(next_position)

    return None


def shortest_path_length(start, goal, width, height, blocked):
    path = shortest_path(start, goal, width, height, blocked)
    if path is None:
        return None
    return len(path) - 1
