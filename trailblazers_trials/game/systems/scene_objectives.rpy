init python:
    import sys

    game_python_root = config.gamedir
    if game_python_root not in sys.path:
        sys.path.insert(0, game_python_root)

    import scene_objectives
    import scene_objectives_data
    import store

    INTERACTIVE_SCENES = scene_objectives_data.INTERACTIVE_SCENES

    def scene_objective_begin(scene_id):
        store.scene_objective_scene_id = scene_id
        store.scene_objective_completed_actions = []

    def scene_objective_current_scene():
        return INTERACTIVE_SCENES[store.scene_objective_scene_id]

    def scene_objective_complete_action(action_id):
        completed = list(store.scene_objective_completed_actions or [])
        if action_id not in completed:
            completed.append(action_id)
        store.scene_objective_completed_actions = completed

    def scene_objective_visible_hotspot_ids():
        return scene_objectives.visible_hotspot_ids(
            scene_objective_current_scene(),
            store.scene_objective_completed_actions,
        )

    def scene_objective_hotspot_data(hotspot_id):
        return scene_objective_current_scene()["hotspots"][hotspot_id]

    def scene_objective_hotspot_state(hotspot_id):
        return scene_objectives.hotspot_state(
            scene_objective_current_scene(),
            hotspot_id,
            store.scene_objective_completed_actions,
        )

    def scene_objective_hotspot_enabled(hotspot_id):
        return scene_objective_hotspot_state(hotspot_id)["enabled"]

    def scene_objective_hotspot_message(hotspot_id):
        return scene_objective_hotspot_state(hotspot_id)["message"]

    def scene_objective_scene_complete():
        return scene_objectives.scene_complete(
            scene_objective_current_scene(),
            store.scene_objective_completed_actions,
        )

    def scene_objective_inventory_summary():
        if hasattr(store, "tb_inventory_summary"):
            return store.tb_inventory_summary()

        return "Inventory: Empty"


screen scene_objective_hotspots():
    modal True
    zorder 80

    $ scene_data = scene_objective_current_scene()

    for hotspot_id in scene_objective_visible_hotspot_ids():
        $ hotspot = scene_objective_hotspot_data(hotspot_id)
        $ hotspot_enabled = scene_objective_hotspot_enabled(hotspot_id)

        button:
            xpos hotspot["xpos"]
            ypos hotspot["ypos"]
            xanchor 0.5
            yanchor 0.5
            xpadding 14
            ypadding 10
            background Solid("#07172bcc" if hotspot_enabled else "#27110fcc")
            hover_background Solid("#174e87ee" if hotspot_enabled else "#6b251fee")
            action Return(hotspot_id)

            hbox:
                spacing 8
                text hotspot["icon"]:
                    style "scene_objective_hotspot_icon"
                text hotspot["label"]:
                    style "scene_objective_hotspot_label"

    frame:
        xalign 0.5
        yalign 0.08
        xmaximum 760
        xpadding 22
        ypadding 14
        background Solid("#04101fd8")

        vbox:
            spacing 5
            text scene_data["title"]:
                style "scene_objective_title"
            text scene_data["objective"]:
                style "scene_objective_prompt"

    frame:
        xalign 0.02
        yalign 0.92
        xmaximum 520
        xpadding 18
        ypadding 12
        background Solid("#04101fd8")

        text scene_objective_inventory_summary():
            style "scene_objective_inventory_text"


style scene_objective_hotspot_icon is default:
    color "#f4fbff"
    size 22
    bold True

style scene_objective_hotspot_label is default:
    color "#f4fbff"
    size 20
    bold True

style scene_objective_title is default:
    color "#f2c76b"
    size 24
    bold True

style scene_objective_prompt is default:
    color "#edf6ff"
    size 17

style scene_objective_inventory_text is default:
    color "#dce7ff"
    size 16
    bold True
