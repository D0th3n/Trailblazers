init python:
    import sys

    game_python_root = config.gamedir
    if game_python_root not in sys.path:
        sys.path.insert(0, game_python_root)

    import combat_data
    import combat_model
    import store

    def turn_battle_start(encounter_id):
        store.turn_battle_state = combat_model.start_battle(
            combat_data.BATTLE_ENCOUNTERS[encounter_id]
        )

    def turn_battle_player():
        return turn_battle_active_actor()

    def turn_battle_party():
        return store.turn_battle_state["party"]

    def turn_battle_active_actor():
        return combat_model.active_actor(store.turn_battle_state)

    def turn_battle_enemy():
        return store.turn_battle_state["enemy"]

    def turn_battle_background():
        return store.turn_battle_state["background"]

    def turn_battle_player_ap_text():
        player = turn_battle_active_actor()
        return "AP %d/%d" % (player["ap"], player["max_ap"])

    def turn_battle_enemy_ap_text():
        enemy_actor = turn_battle_enemy()
        return "AP %d/%d" % (enemy_actor["ap"], enemy_actor["max_ap"])

    def turn_battle_action_ids():
        return store.turn_battle_state["player_actions"]

    def turn_battle_action_data(action_id):
        return store.turn_battle_state["actions"][action_id]

    def turn_battle_action_enabled(action_id):
        player = turn_battle_active_actor()
        action = turn_battle_action_data(action_id)
        return player["ap"] >= action.get("cost", 0)

    def turn_battle_log_lines():
        return store.turn_battle_state["log"][-4:]

    def turn_battle_outcome():
        return store.turn_battle_state.get("outcome")

    def turn_battle_resolve_player_action(action_id):
        store.turn_battle_state = combat_model.resolve_player_action(
            store.turn_battle_state,
            action_id,
        )


label turn_battle(encounter_id):

    $ turn_battle_encounter_id = encounter_id
    $ turn_battle_start(encounter_id)

    jump turn_battle_loop


label turn_battle_loop:

    call screen turn_battle_screen

    $ turn_battle_choice = _return

    if turn_battle_choice == "leave":
        return

    if turn_battle_choice == "retry":
        $ turn_battle_start(turn_battle_encounter_id)
        jump turn_battle_loop

    $ turn_battle_resolve_player_action(turn_battle_choice)

    if turn_battle_outcome() == "victory":
        call screen turn_battle_screen
        return

    if turn_battle_outcome() == "defeat":
        call screen turn_battle_screen
        return

    jump turn_battle_loop


screen turn_battle_ap_meter(actor):
    hbox:
        spacing 8
        for slot in range(actor["max_ap"]):
            frame:
                xsize 52
                ysize 20
                background Solid("#7b43e8f0" if slot < actor["ap"] else "#26333dcc")


screen turn_battle_action_row(action_id=None, label="", key_hint="", cost_text="", enabled=True):
    button:
        style "turn_battle_action_row_button"
        sensitive enabled
        if action_id is not None:
            action Return(action_id)
        else:
            action NullAction()

        fixed:
            xsize 315
            ysize 44

            text key_hint:
                style "turn_battle_action_key"
                xpos 8
                yalign 0.5

            text label:
                style "turn_battle_action_row_text"
                xpos 58
                yalign 0.5

            if cost_text:
                text cost_text:
                    style "turn_battle_action_cost"
                    xalign 0.94
                    yalign 0.5


screen turn_battle_screen():
    modal True
    zorder 90

    $ player = turn_battle_active_actor()
    $ party = turn_battle_party()
    $ enemy_actor = turn_battle_enemy()
    $ outcome = turn_battle_outcome()

    add Transform(turn_battle_background(), xysize=(1600, 900))
    add Solid("#02071478")

    add enemy_actor["sprite"] at turn_battle_enemy_sprite

    for party_actor in party:
        if party_actor.get("sprite"):
            add party_actor["sprite"] at turn_battle_party_sprite(party_actor["slot_index"])

    if outcome is None:
        use turn_battle_player_action_hotspot(player, outcome)

    frame:
        style "turn_battle_enemy_top_panel"

        vbox:
            spacing 5
            text "Brawler":
                style "turn_battle_top_name"
            hbox:
                spacing 14
                use turn_battle_ap_meter(enemy_actor)
                text turn_battle_enemy_ap_text():
                    style "turn_battle_ap_text"
            text "Stock":
                style "turn_battle_stock_text"
            text "Heavy":
                style "turn_battle_role_text"

    frame:
        style "turn_battle_player_top_panel"

        vbox:
            spacing 5
            text "Use Consumable Items":
                style "turn_battle_hint_text"
            text "Player":
                style "turn_battle_top_name"
            hbox:
                spacing 14
                text turn_battle_player_ap_text():
                    style "turn_battle_ap_text"
                use turn_battle_ap_meter(player)
            text "Stock":
                style "turn_battle_stock_text"

    if outcome is None:
        if turn_battle_action_enabled("attack"):
            key "K_a" action Return("attack")
        if turn_battle_action_enabled("ember_focus"):
            key "K_f" action Return("ember_focus")
        key "K_s" action Return("focus")
        if turn_battle_action_enabled("guard"):
            key "K_d" action Return("guard")

        frame:
            style "turn_battle_command_panel"

            vbox:
                spacing 4
                text "Action Menu":
                    style "turn_battle_command_title"

                use turn_battle_action_row(
                    action_id="attack",
                    label="Attack",
                    key_hint="A",
                    cost_text="-1 AP",
                    enabled=turn_battle_action_enabled("attack"),
                )
                use turn_battle_action_row(
                    action_id="ember_focus",
                    label="Feats",
                    key_hint="F",
                    cost_text="-2 AP",
                    enabled=turn_battle_action_enabled("ember_focus"),
                )
                use turn_battle_action_row(
                    label="Magic",
                    key_hint="W",
                    cost_text="MENU",
                    enabled=False,
                )
                use turn_battle_action_row(
                    action_id="focus",
                    label="Support",
                    key_hint="S",
                    cost_text="+3 AP",
                    enabled=turn_battle_action_enabled("focus"),
                )
                use turn_battle_action_row(
                    label="Items",
                    key_hint="R",
                    cost_text="MENU",
                    enabled=False,
                )
                use turn_battle_action_row(
                    action_id="guard",
                    label="Defense",
                    key_hint="D",
                    cost_text="-1 AP",
                    enabled=turn_battle_action_enabled("guard"),
                )
    else:
        $ outcome_label = "Training Complete" if outcome == "victory" else "Training Failed"

        frame:
            style "turn_battle_command_panel"

            vbox:
                spacing 10
                text outcome_label:
                    style "turn_battle_outcome_text"
                textbutton "Return":
                    style "turn_battle_return_button"
                    action Return("leave")
                textbutton "Retry":
                    style "turn_battle_return_button"
                    action Return("retry")
                textbutton "Exit Training":
                    style "turn_battle_return_button"
                    action Return("leave")

    frame:
        style "turn_battle_message_panel"

        vbox:
            spacing 6
            for line in turn_battle_log_lines():
                text line:
                    style "turn_battle_log_text"

    frame:
        style "turn_battle_bottom_left_panel"

        hbox:
            spacing 22
            text "Offense":
                style "turn_battle_bottom_heading"
            text "[enemy_actor['hp']]/[enemy_actor['max_hp']]":
                style "turn_battle_bottom_stat"

    frame:
        style "turn_battle_bottom_center_panel"

        text "RAKIA":
            style "turn_battle_location_text"

    frame:
        style "turn_battle_status_panel"

        use turn_battle_party_status(party)


screen turn_battle_party_status(party):
    hbox:
        spacing 24

        for party_actor in party:
            vbox:
                spacing 5
                text party_actor["name"]:
                    style "turn_battle_actor_name"
                text "HP [party_actor['hp']] / [party_actor['max_hp']]":
                    style "turn_battle_stat_text"

        vbox:
            spacing 5
            text "MP --":
                style "turn_battle_future_stat_text"
            text "STA --":
                style "turn_battle_future_stat_text"
            text "CHAOS --":
                style "turn_battle_future_stat_text"


screen turn_battle_player_action_hotspot(player, outcome):
    button:
        xpos 1160
        ypos 310
        xsize 220
        ysize 310
        background Solid("#00000000")
        hover_background Solid("#69b7ff26")
        action ToggleScreen("turn_battle_player_quick_actions")


screen turn_battle_player_quick_actions():
    zorder 110

    frame:
        style "turn_battle_player_quick_panel"

        vbox:
            spacing 7

            text "Oren":
                style "turn_battle_player_quick_title"

            textbutton "Attack":
                style "turn_battle_player_quick_button"
                sensitive turn_battle_action_enabled("attack")
                action [Hide("turn_battle_player_quick_actions"), Return("attack")]

            textbutton "Feats":
                style "turn_battle_player_quick_button"
                sensitive turn_battle_action_enabled("ember_focus")
                action [Hide("turn_battle_player_quick_actions"), Return("ember_focus")]

            textbutton "Support":
                style "turn_battle_player_quick_button"
                sensitive turn_battle_action_enabled("focus")
                action [Hide("turn_battle_player_quick_actions"), Return("focus")]

            textbutton "Defense":
                style "turn_battle_player_quick_button"
                sensitive turn_battle_action_enabled("guard")
                action [Hide("turn_battle_player_quick_actions"), Return("guard")]

            textbutton "Close":
                style "turn_battle_player_quick_close_button"
                action Hide("turn_battle_player_quick_actions")


transform turn_battle_player_sprite:
    xalign 0.78
    yalign 0.64
    zoom 0.92

transform turn_battle_party_sprite(slot_index=0):
    xalign 0.78
    yalign 0.64 + (slot_index * 0.09)
    zoom 0.92

transform turn_battle_enemy_sprite:
    xalign 0.22
    yalign 0.64
    xzoom -1.0
    zoom 0.88


style turn_battle_enemy_top_panel:
    background Solid("#071a36aa")
    xpos 70
    ypos 38
    xsize 470
    xpadding 12
    ypadding 8

style turn_battle_player_top_panel:
    background Solid("#071a36aa")
    xpos 1058
    ypos 30
    xsize 470
    xpadding 12
    ypadding 8

style turn_battle_command_panel:
    background Solid("#071a36a8")
    xpos 800
    ypos 252
    xsize 380
    xpadding 18
    ypadding 12

style turn_battle_message_panel:
    background Solid("#061225d0")
    xpos 475
    ypos 735
    xsize 650
    ysize 88
    xpadding 20
    ypadding 12

style turn_battle_bottom_left_panel:
    background Solid("#342c9fcc")
    xpos 68
    ypos 660
    xsize 650
    ysize 74
    xpadding 26
    ypadding 14

style turn_battle_bottom_center_panel:
    background Solid("#11152ccc")
    xalign 0.5
    ypos 681
    xsize 145
    ysize 36
    xpadding 10
    ypadding 4

style turn_battle_status_panel:
    background Solid("#342c9fcc")
    xpos 890
    ypos 660
    xsize 642
    ysize 74
    xpadding 26
    ypadding 12

style turn_battle_player_quick_panel:
    background Solid("#071a36e8")
    xpos 1188
    ypos 210
    xsize 245
    xpadding 14
    ypadding 12

style turn_battle_player_quick_title is default:
    color "#ffffff"
    size 23
    bold True
    xalign 0.5

style turn_battle_player_quick_button:
    background Solid("#1b2f65d8")
    hover_background Solid("#3657bae8")
    insensitive_background Solid("#1b253ecc")
    xminimum 215
    left_padding 12
    right_padding 12
    top_padding 7
    bottom_padding 7

style turn_battle_player_quick_button_text:
    color "#f9fbff"
    hover_color "#ffffff"
    insensitive_color "#8d9aba"
    size 19
    bold True

style turn_battle_player_quick_close_button:
    background Solid("#0c1730d8")
    hover_background Solid("#203f7ee8")
    xminimum 215
    left_padding 12
    right_padding 12
    top_padding 6
    bottom_padding 6

style turn_battle_player_quick_close_button_text:
    color "#cbd5ff"
    hover_color "#ffffff"
    size 16
    bold True

style turn_battle_top_name is default:
    color "#ffffff"
    size 25
    bold True

style turn_battle_hint_text is default:
    color "#ffffff"
    size 16

style turn_battle_ap_text is default:
    color "#ffffff"
    size 22
    bold True

style turn_battle_stock_text is default:
    color "#f0d46b"
    size 24
    bold True

style turn_battle_role_text is default:
    color "#d7dcff"
    size 17

style turn_battle_command_title is default:
    color "#f7f3ff"
    size 22
    bold True
    xalign 0.5

style turn_battle_action_row_button:
    background Solid("#1b2f65d8")
    hover_background Solid("#3657bae8")
    insensitive_background Solid("#1b253ecc")
    left_padding 0
    right_padding 0
    top_padding 0
    bottom_padding 0

style turn_battle_action_key is default:
    color "#d7e4ff"
    size 15
    bold True

style turn_battle_action_row_text is default:
    color "#f9fbff"
    insensitive_color "#8d9aba"
    size 22
    bold True

style turn_battle_action_cost is default:
    color "#dce7ff"
    insensitive_color "#788398"
    size 14
    bold True

style turn_battle_actor_name is default:
    color "#f8fbff"
    size 20
    bold True

style turn_battle_stat_text is default:
    color "#ffffff"
    size 19
    bold True

style turn_battle_future_stat_text is default:
    color "#cbd5ff"
    size 16
    bold True

style turn_battle_log_text is default:
    color "#f1f6ff"
    size 16

style turn_battle_bottom_heading is default:
    color "#ffffff"
    size 30
    bold True

style turn_battle_bottom_stat is default:
    color "#ffffff"
    size 25
    bold True

style turn_battle_location_text is default:
    color "#d5defe"
    size 21
    bold True
    xalign 0.5

style turn_battle_outcome_text is default:
    color "#f5c85d"
    size 24
    bold True

style turn_battle_return_button:
    background Solid("#1b2f65d8")
    hover_background Solid("#3657bae8")
    xminimum 250
    left_padding 12
    right_padding 12
    top_padding 8
    bottom_padding 8

style turn_battle_return_button_text:
    color "#f8fbff"
    hover_color "#ffffff"
    size 22
    bold True
