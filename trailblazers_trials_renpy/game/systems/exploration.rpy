init python:
    import sys

    game_python_root = config.gamedir
    if game_python_root not in sys.path:
        sys.path.insert(0, game_python_root)

    import exploration_data
    import exploration_model
    import store

    EXPLORATION_MAPS = exploration_data.EXPLORATION_MAPS

    def exploration_begin(map_id, reset_position=False):
        store.exploration_map_id = map_id
        store.exploration_result = None
        store.exploration_pending_event = None
        store.exploration_path = []

    def exploration_current_map():
        return EXPLORATION_MAPS[store.exploration_map_id]

    def exploration_event_flag_name(event_name):
        return exploration_current_map().get("completion_flags", {}).get(event_name)

    def exploration_event_complete(event_name):
        flag_name = exploration_event_flag_name(event_name)
        if not flag_name:
            return False
        return bool(getattr(store, flag_name, False))

    def exploration_visible_event_names():
        visible = []
        for event_name in exploration_current_map().get("quest_order", []):
            if exploration_event_complete(event_name):
                continue
            visible.append(event_name)
        return visible

    def exploration_marker_position(event_name):
        return exploration_current_map()["marker_positions"][event_name]

    def exploration_context_text():
        map_data = exploration_current_map()
        main_event = map_data["main_event"]
        main_title = map_data["event_titles"][main_event]

        if exploration_event_complete("well") and exploration_event_complete("villager"):
            return "You have the village clues. Click %s to continue the story." % main_title

        return "Click a marker on the village overview to choose where Oren investigates next."

    def exploration_progress_text():
        progress = []
        for event_name in exploration_current_map().get("quest_order", []):
            if exploration_event_complete(event_name):
                progress.append(exploration_current_map()["event_short_labels"][event_name])

        if not progress:
            return "No side investigations finished yet."

        return "Completed: %s." % ", ".join(progress)

    def exploration_quest_entries():
        map_data = exploration_current_map()
        entries = []

        for event_name in map_data.get("quest_order", []):
            is_main = event_name == map_data.get("main_event")
            done = exploration_event_complete(event_name)
            title = map_data["event_titles"][event_name]
            if is_main:
                status = "MAIN"
            elif done:
                status = "DONE"
            else:
                status = "SIDE"
            entries.append((status, title))

        return entries

    def exploration_quest_label(status, title):
        return exploration_model.format_quest_log_entry(status, title)


screen exploration_screen():
    modal True
    zorder 100

    $ map_data = exploration_current_map()

    add map_data["background"]

    for event_name in exploration_visible_event_names():
        $ marker_x, marker_y = exploration_marker_position(event_name)

        button:
            xpos marker_x
            ypos marker_y
            xanchor 0.5
            yanchor 0.5
            xpadding 18
            ypadding 10
            background Solid("#1d0d08ee")
            hover_background Solid("#5c3218ee")
            action Return(event_name)

            vbox:
                spacing 1
                xalign 0.5
                text map_data["event_markers"][event_name] color "#f7dd9b" size 26 xalign 0.5
                text map_data["event_short_labels"][event_name] color "#fff6df" size 18 xalign 0.5

    frame:
        background Solid("#140d09d8")
        xalign 0.5
        yalign 0.03
        xmaximum 1120
        xpadding 20
        ypadding 12

        vbox:
            spacing 4
            text "Anozira Village Investigation" color "#f7dd9b" size 24
            text map_data["objective"] color "#f3ebe3" size 16

    frame:
        background Solid("#140d09d8")
        xalign 0.87
        yalign 0.06
        xmaximum 440
        xpadding 18
        ypadding 14

        vbox:
            spacing 4
            text "Quest Log" color "#f7dd9b" size 22
            for status, title in exploration_quest_entries():
                text exploration_quest_label(status, title) color "#f3ebe3" size 15

    frame:
        background Solid("#140d09d8")
        xalign 0.5
        yalign 0.94
        xmaximum 1160
        xpadding 20
        ypadding 12

        vbox:
            spacing 4
            text exploration_context_text() color "#f3ebe3" size 16
            text exploration_progress_text() color "#f0d8b8" size 14
            text "Mouse only: click a marker to inspect that location or continue to Embrum." color "#d8c8bf" size 13
