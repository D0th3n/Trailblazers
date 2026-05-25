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
            combat_data.BATTLE_ENCOUNTERS[encounter_id],
            inventory=store.tb_inventory,
        )

    def turn_battle_player():
        return turn_battle_active_actor()

    def turn_battle_party():
        return store.turn_battle_state["party"]

    def turn_battle_active_actor():
        return combat_model.active_actor(store.turn_battle_state)

    def turn_battle_enemy():
        return combat_model.primary_enemy(store.turn_battle_state)

    def turn_battle_enemies():
        return store.turn_battle_state["enemies"]

    def turn_battle_background():
        return store.turn_battle_state["background"]

    def turn_battle_player_ap_text():
        player = turn_battle_active_actor()
        return "AP %d/%d" % (player["ap"], player["max_ap"])

    def turn_battle_actor_ap_text(actor):
        return "AP %d / %d" % (actor.get("ap", 0), actor.get("max_ap", 0))

    def turn_battle_actor_hp_text(actor):
        return "HP %d / %d" % (actor.get("hp", 0), actor.get("max_hp", 0))

    def turn_battle_last_action():
        return store.turn_battle_state.get("last_action")

    def turn_battle_last_action_value(key, default=None):
        action = turn_battle_last_action()
        if not action:
            return default

        return action.get(key, default)

    def turn_battle_actor_lunge_x(actor):
        action = turn_battle_last_action()
        if not action or action.get("actor_id") != actor["id"]:
            return 0

        if actor.get("team") == "party":
            return -34

        return 34

    def turn_battle_actor_recoil_x(actor):
        action = turn_battle_last_action()
        if not action or action.get("target_id") != actor["id"]:
            return 0

        if action.get("damage", 0) <= 0:
            return 0

        if actor.get("team") == "party":
            return 24

        return -24

    def turn_battle_freeze_alpha(actor):
        action = turn_battle_last_action()
        if (
            action
            and action.get("target_id") == actor["id"]
            and action.get("action_id") == "freeze_ray"
        ):
            return 0.82

        return 1.0

    def turn_battle_actor_screen_x(actor):
        if actor.get("team") == "enemy":
            return 360 + (actor.get("slot_index", 0) * 160)

        return 1180 - (actor.get("slot_index", 0) * 130)

    def turn_battle_actor_screen_y(actor):
        if actor.get("team") == "enemy":
            return 455 - (actor.get("slot_index", 0) * 45)

        return 460 + (actor.get("slot_index", 0) * 35)

    def turn_battle_party_actor_name(actor):
        if actor["id"] == turn_battle_active_actor()["id"]:
            return "> %s" % actor["name"]

        return actor["name"]

    def turn_battle_enemy_ap_text():
        enemy_actor = turn_battle_enemy()
        return "AP %d/%d" % (enemy_actor["ap"], enemy_actor["max_ap"])

    def turn_battle_action_ids():
        return store.turn_battle_state["player_actions"]

    def turn_battle_action_data(action_id):
        return combat_model.action_for_actor(
            store.turn_battle_state,
            turn_battle_active_actor(),
            action_id,
        )

    def turn_battle_action_label(action_id):
        return turn_battle_action_data(action_id).get("label", "")

    def turn_battle_action_enabled(action_id):
        return combat_model.action_can_be_used(store.turn_battle_state, action_id)

    def turn_battle_action_uses_text(action_id):
        limit = combat_model.action_use_capacity(store.turn_battle_state, action_id)
        if limit is None:
            return "--/--"

        remaining = combat_model.action_uses_remaining(
            store.turn_battle_state,
            action_id,
        )
        return "%d/%d" % (remaining, limit)

    def turn_battle_action_cost_text(action_id):
        action = turn_battle_action_data(action_id)
        if action.get("use_capacity"):
            return "ITEM"

        restores_ap = action.get("restores_ap", 0)
        if restores_ap:
            return "+%d AP" % restores_ap

        restores_qana = action.get("restores_qana", 0)
        if restores_qana:
            return "+%d Q" % restores_qana

        qana_cost = action.get("qana_cost", 0)
        stamina_cost = action.get("stamina_cost", 0)
        chaos_gain = action.get("chaos_gain", 0)
        cost = action.get("cost", 0)
        parts = []
        if cost:
            parts.append("%dAP" % cost)
        if qana_cost:
            parts.append("%dQ" % qana_cost)
        if stamina_cost:
            parts.append("%dSTA" % stamina_cost)
        if chaos_gain:
            parts.append("+%dCH" % chaos_gain)

        if parts:
            return " ".join(parts)

        return "0 AP"

    def turn_battle_player_stamina_text(actor):
        return "STA %d / %d" % (
            actor.get("stamina", 0),
            actor.get("max_stamina", 0),
        )

    def turn_battle_player_chaos_text(actor):
        return "CHAOS %d / %d" % (
            actor.get("chaos", 0),
            actor.get("max_chaos", 0),
        )

    def turn_battle_player_qana_text(actor):
        return "QANA %d / %d" % (actor.get("qana", 0), actor.get("max_qana", 0))

    def turn_battle_prompt_title():
        if turn_battle_pending_round_start():
            return "Round %d Complete" % store.turn_battle_state.get("round", 1)

        if store.turn_battle_state.get("actions_taken", 0) == 0:
            return "Battle Start"

        return "Round %d" % store.turn_battle_state.get("round", 1)

    def turn_battle_prompt_text():
        if turn_battle_pending_round_start():
            return "Advance when you are ready."

        actor = turn_battle_active_actor()
        return "Click %s to choose an action." % actor["name"]

    def turn_battle_pending_round_start():
        return store.turn_battle_state.get("pending_round_start", False)

    def turn_battle_dragon_spells_enabled():
        actor = turn_battle_active_actor()
        return actor.get("allow_dragon_spells", False)

    def turn_battle_hotspot_x(actor):
        return 1160 - (actor.get("slot_index", 0) * 120)

    def turn_battle_hotspot_y(actor):
        return 310 + (actor.get("slot_index", 0) * 30)

    def turn_battle_log_lines():
        return store.turn_battle_state["log"][-4:]

    def turn_battle_outcome():
        return store.turn_battle_state.get("outcome")

    def turn_battle_resolve_player_action(action_id):
        store.turn_battle_state = combat_model.resolve_player_action(
            store.turn_battle_state,
            action_id,
        )
        store.tb_inventory = dict(store.turn_battle_state.get("inventory_counts", {}))

    def turn_battle_begin_pending_round():
        store.turn_battle_state = combat_model.begin_pending_round(
            store.turn_battle_state,
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

    if turn_battle_choice == "next_round":
        $ turn_battle_begin_pending_round()
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


screen turn_battle_action_row(
    action_id=None,
    label="",
    key_hint="",
    cost_text="",
    uses_text="",
    enabled=True,
    row_width=315,
    hide_quick=False,
    submenu=None,
):
    button:
        style "turn_battle_action_row_button"
        sensitive enabled
        if action_id is not None:
            if hide_quick:
                action [Hide("turn_battle_player_quick_actions"), Return(action_id)]
            else:
                action Return(action_id)
        elif submenu is not None:
            action SetScreenVariable("submenu", submenu)
        else:
            action NullAction()

        fixed:
            xsize row_width
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

            if uses_text:
                text uses_text:
                    style "turn_battle_action_uses"
                    xalign 0.73
                    yalign 0.5


screen turn_battle_screen():
    modal True
    zorder 90

    $ player = turn_battle_active_actor()
    $ party = turn_battle_party()
    $ enemies = turn_battle_enemies()
    $ enemy_actor = turn_battle_enemy()
    $ outcome = turn_battle_outcome()

    add Transform(turn_battle_background(), xysize=(1600, 900))
    add Solid("#02071478")

    for enemy_index, enemy_entry in enumerate(enemies):
        add enemy_entry["sprite"] at turn_battle_enemy_sprite(enemy_index), turn_battle_idle_bob, turn_battle_actor_lunge(enemy_entry), turn_battle_actor_recoil(enemy_entry), turn_battle_freeze_hitstun(enemy_entry)

    for party_actor in party:
        if party_actor.get("sprite"):
            if party_actor["sprite"] == "combat oren idle":
                add party_actor["sprite"] at turn_battle_party_sprite(party_actor["slot_index"]), turn_battle_actor_lunge(party_actor), turn_battle_actor_recoil(party_actor), turn_battle_freeze_hitstun(party_actor)
            else:
                add party_actor["sprite"] at turn_battle_party_sprite(party_actor["slot_index"]), turn_battle_idle_bob, turn_battle_actor_lunge(party_actor), turn_battle_actor_recoil(party_actor), turn_battle_freeze_hitstun(party_actor)

    use turn_battle_vfx(party, enemies)

    if outcome is None and not turn_battle_pending_round_start():
        use turn_battle_player_action_hotspot(player, outcome)

    for enemy_index, enemy_entry in enumerate(enemies):
        frame:
            style "turn_battle_enemy_top_panel"
            ypos 28 + (enemy_index * 142)

            vbox:
                spacing 5
                text enemy_entry["name"]:
                    style "turn_battle_top_name"
                text "Training Dummy":
                    style "turn_battle_stock_text"
                use turn_battle_enemy_status(enemy_entry, show_meter=True)

    frame:
        style "turn_battle_player_top_panel"

        vbox:
            spacing 5
            text "Use Consumable Items":
                style "turn_battle_hint_text"
            text player["name"]:
                style "turn_battle_top_name"
            hbox:
                spacing 14
                text turn_battle_player_ap_text():
                    style "turn_battle_ap_text"
                use turn_battle_ap_meter(player)
            text "Stock":
                style "turn_battle_stock_text"

    if outcome is None and turn_battle_pending_round_start():
        frame:
            style "turn_battle_command_panel"

            vbox:
                spacing 10
                text turn_battle_prompt_title():
                    style "turn_battle_command_title"
                text turn_battle_prompt_text():
                    style "turn_battle_prompt_text"
                textbutton "Next Round":
                    style "turn_battle_return_button"
                    action Return("next_round")
    elif outcome is None:
        frame:
            style "turn_battle_prompt_panel"

            vbox:
                spacing 8
                text turn_battle_prompt_title():
                    style "turn_battle_command_title"
                text turn_battle_prompt_text():
                    style "turn_battle_prompt_text"
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

        use turn_battle_enemy_status(enemy_actor)

    frame:
        style "turn_battle_bottom_center_panel"

        text "VS":
            style "turn_battle_location_text"

    frame:
        style "turn_battle_status_panel"

        use turn_battle_party_status(party)


screen turn_battle_party_status(party):
    hbox:
        spacing 24

        for party_actor in party:
            hbox:
                spacing 32

                vbox:
                    spacing 5
                    text turn_battle_party_actor_name(party_actor):
                        style "turn_battle_actor_name"
                    text "HP [party_actor['hp']] / [party_actor['max_hp']]":
                        style "turn_battle_stat_text"
                    text turn_battle_actor_ap_text(party_actor):
                        style "turn_battle_stat_text"

                vbox:
                    spacing 3
                    text turn_battle_player_qana_text(party_actor):
                        style "turn_battle_future_stat_text"
                    text turn_battle_player_stamina_text(party_actor):
                        style "turn_battle_future_stat_text"
                    text turn_battle_player_chaos_text(party_actor):
                        style "turn_battle_future_stat_text"


screen turn_battle_enemy_status(enemy_actor, show_meter=False):
    vbox:
        spacing 4

        if show_meter:
            hbox:
                spacing 12
                text turn_battle_actor_ap_text(enemy_actor):
                    style "turn_battle_stat_text"
                use turn_battle_ap_meter(enemy_actor)

        hbox:
            spacing 28

            vbox:
                spacing 5
                text turn_battle_actor_hp_text(enemy_actor):
                    style "turn_battle_stat_text"
                if not show_meter:
                    text turn_battle_actor_ap_text(enemy_actor):
                        style "turn_battle_stat_text"

            vbox:
                spacing 3
                text turn_battle_player_qana_text(enemy_actor):
                    style "turn_battle_future_stat_text"
                text turn_battle_player_stamina_text(enemy_actor):
                    style "turn_battle_future_stat_text"
                text turn_battle_player_chaos_text(enemy_actor):
                    style "turn_battle_future_stat_text"


screen turn_battle_vfx(party, enemies):
    $ action = turn_battle_last_action()

    if action:
        $ actor_x = 0
        $ actor_y = 0
        $ target_x = 0
        $ target_y = 0
        for candidate in party + enemies:
            if candidate["id"] == action.get("actor_id"):
                $ actor_x = turn_battle_actor_screen_x(candidate)
                $ actor_y = turn_battle_actor_screen_y(candidate)
            if candidate["id"] == action.get("target_id"):
                $ target_x = turn_battle_actor_screen_x(candidate)
                $ target_y = turn_battle_actor_screen_y(candidate)

        if action.get("action_id") == "freeze_ray":
            frame:
                style "turn_battle_freeze_beam"
                xpos min(actor_x, target_x)
                ypos min(actor_y, target_y) + 32
                xsize max(120, abs(target_x - actor_x))
                at turn_battle_beam_flash
        elif action.get("action_id") == "fire_ball":
            frame:
                style "turn_battle_fire_orb"
                xpos target_x - 22
                ypos target_y + 12
                at turn_battle_impact_flash
        elif action.get("action_id") in ("dragon_geisure", "dragon_javelin"):
            frame:
                style "turn_battle_dragon_eruption"
                xpos target_x - 50
                ypos target_y + 55
                at turn_battle_impact_flash

        if action.get("action_label"):
            text action["action_label"]:
                style "turn_battle_cast_label"
                xpos actor_x - 70
                ypos actor_y - 90
                at turn_battle_float_label

        if action.get("damage", 0) > 0:
            text "-%d" % action["damage"]:
                style "turn_battle_damage_number"
                xpos target_x - 25
                ypos target_y - 70
                at turn_battle_float_label


screen turn_battle_player_action_hotspot(player, outcome):
    button:
        xpos turn_battle_hotspot_x(player)
        ypos turn_battle_hotspot_y(player)
        xsize 220
        ysize 310
        background Solid("#00000000")
        hover_background Solid("#69b7ff26")
        action ToggleScreen("turn_battle_player_quick_actions")


screen turn_battle_player_quick_actions():
    zorder 110
    default submenu = "main"

    frame:
        style "turn_battle_player_quick_panel"

        vbox:
            spacing 7

            $ quick_actor = turn_battle_active_actor()
            $ submenu_title = quick_actor["name"] if submenu == "main" else ("Qana" if submenu == "qana" else ("Dragon Spells" if submenu == "dragon" else ("Defense" if submenu == "defense" else "Items")))

            text submenu_title:
                style "turn_battle_player_quick_title"

            if submenu == "main":
                use turn_battle_action_row(
                    action_id="attack",
                    label=turn_battle_action_label("attack"),
                    cost_text=turn_battle_action_cost_text("attack"),
                    uses_text=turn_battle_action_uses_text("attack"),
                    enabled=turn_battle_action_enabled("attack"),
                    row_width=342,
                    hide_quick=True,
                )

                use turn_battle_action_row(
                    action_id="ember_focus",
                    label=turn_battle_action_label("ember_focus"),
                    cost_text=turn_battle_action_cost_text("ember_focus"),
                    uses_text=turn_battle_action_uses_text("ember_focus"),
                    enabled=turn_battle_action_enabled("ember_focus"),
                    row_width=342,
                    hide_quick=True,
                )

                use turn_battle_action_row(
                    label="Qana",
                    cost_text="MENU",
                    submenu="qana",
                    enabled=True,
                    row_width=342,
                )

                use turn_battle_action_row(
                    action_id="focus",
                    label=turn_battle_action_label("focus"),
                    cost_text=turn_battle_action_cost_text("focus"),
                    uses_text=turn_battle_action_uses_text("focus"),
                    enabled=turn_battle_action_enabled("focus"),
                    row_width=342,
                    hide_quick=True,
                )

                use turn_battle_action_row(
                    label="Items",
                    cost_text="MENU",
                    submenu="items",
                    enabled=True,
                    row_width=342,
                )

                use turn_battle_action_row(
                    label="Defense",
                    cost_text="MENU",
                    submenu="defense",
                    enabled=True,
                    row_width=342,
                )
            elif submenu == "qana":
                use turn_battle_action_row(
                    action_id="fire_ball",
                    label=turn_battle_action_label("fire_ball"),
                    cost_text=turn_battle_action_cost_text("fire_ball"),
                    uses_text=turn_battle_action_uses_text("fire_ball"),
                    enabled=turn_battle_action_enabled("fire_ball"),
                    row_width=342,
                    hide_quick=True,
                )

                use turn_battle_action_row(
                    action_id="healing_burst",
                    label=turn_battle_action_label("healing_burst"),
                    cost_text=turn_battle_action_cost_text("healing_burst"),
                    uses_text=turn_battle_action_uses_text("healing_burst"),
                    enabled=turn_battle_action_enabled("healing_burst"),
                    row_width=342,
                    hide_quick=True,
                )

                use turn_battle_action_row(
                    action_id="freeze_ray",
                    label=turn_battle_action_label("freeze_ray"),
                    cost_text=turn_battle_action_cost_text("freeze_ray"),
                    uses_text=turn_battle_action_uses_text("freeze_ray"),
                    enabled=turn_battle_action_enabled("freeze_ray"),
                    row_width=342,
                    hide_quick=True,
                )

                use turn_battle_action_row(
                    label="Dragon Spells",
                    cost_text="MENU",
                    submenu="dragon",
                    enabled=turn_battle_dragon_spells_enabled(),
                    row_width=342,
                )

                textbutton "Back":
                    style "turn_battle_player_quick_close_button"
                    action SetScreenVariable("submenu", "main")
            elif submenu == "dragon":
                use turn_battle_action_row(
                    action_id="dragon_geisure",
                    label=turn_battle_action_label("dragon_geisure"),
                    cost_text=turn_battle_action_cost_text("dragon_geisure"),
                    uses_text=turn_battle_action_uses_text("dragon_geisure"),
                    enabled=turn_battle_action_enabled("dragon_geisure"),
                    row_width=342,
                    hide_quick=True,
                )

                use turn_battle_action_row(
                    action_id="dragon_javelin",
                    label=turn_battle_action_label("dragon_javelin"),
                    cost_text=turn_battle_action_cost_text("dragon_javelin"),
                    uses_text=turn_battle_action_uses_text("dragon_javelin"),
                    enabled=turn_battle_action_enabled("dragon_javelin"),
                    row_width=342,
                    hide_quick=True,
                )

                textbutton "Back":
                    style "turn_battle_player_quick_close_button"
                    action SetScreenVariable("submenu", "qana")
            elif submenu == "defense":
                use turn_battle_action_row(
                    action_id="guard",
                    label=turn_battle_action_label("guard"),
                    cost_text=turn_battle_action_cost_text("guard"),
                    uses_text=turn_battle_action_uses_text("guard"),
                    enabled=turn_battle_action_enabled("guard"),
                    row_width=342,
                    hide_quick=True,
                )

                use turn_battle_action_row(
                    action_id="dodge",
                    label=turn_battle_action_label("dodge"),
                    cost_text=turn_battle_action_cost_text("dodge"),
                    uses_text=turn_battle_action_uses_text("dodge"),
                    enabled=turn_battle_action_enabled("dodge"),
                    row_width=342,
                    hide_quick=True,
                )

                textbutton "Back":
                    style "turn_battle_player_quick_close_button"
                    action SetScreenVariable("submenu", "main")
            elif submenu == "items":
                use turn_battle_action_row(
                    action_id="health_elixir",
                    label=turn_battle_action_label("health_elixir"),
                    cost_text=turn_battle_action_cost_text("health_elixir"),
                    uses_text=turn_battle_action_uses_text("health_elixir"),
                    enabled=turn_battle_action_enabled("health_elixir"),
                    row_width=342,
                    hide_quick=True,
                )

                use turn_battle_action_row(
                    action_id="qana_elixir",
                    label=turn_battle_action_label("qana_elixir"),
                    cost_text=turn_battle_action_cost_text("qana_elixir"),
                    uses_text=turn_battle_action_uses_text("qana_elixir"),
                    enabled=turn_battle_action_enabled("qana_elixir"),
                    row_width=342,
                    hide_quick=True,
                )

                textbutton "Back":
                    style "turn_battle_player_quick_close_button"
                    action SetScreenVariable("submenu", "main")

            textbutton "Close":
                style "turn_battle_player_quick_close_button"
                action Hide("turn_battle_player_quick_actions")


transform turn_battle_player_sprite:
    xalign 0.78
    yalign 0.64
    zoom 0.92

transform turn_battle_party_sprite(slot_index=0):
    xalign 0.78 - (slot_index * 0.07)
    yalign 0.64 + (slot_index * 0.04)
    zoom 0.92 - (slot_index * 0.12)

transform turn_battle_enemy_sprite(slot_index=0):
    xalign 0.22 + (slot_index * 0.10)
    yalign 0.64 - (slot_index * 0.06)
    xzoom -1.0
    zoom 0.88

transform turn_battle_idle_bob:
    yoffset 0
    ease 1.0 yoffset -5
    ease 1.0 yoffset 0
    repeat

transform turn_battle_actor_lunge(actor):
    xoffset 0
    easein 0.08 xoffset turn_battle_actor_lunge_x(actor)
    easeout 0.16 xoffset 0

transform turn_battle_actor_recoil(actor):
    xoffset 0
    easein 0.06 xoffset turn_battle_actor_recoil_x(actor)
    easeout 0.18 xoffset 0

transform turn_battle_freeze_hitstun(actor):
    alpha 1.0
    block:
        alpha turn_battle_freeze_alpha(actor)
        pause 0.08
        alpha 1.0
        pause 0.08
        repeat 2

transform turn_battle_beam_flash:
    alpha 0.0
    linear 0.05 alpha 0.9
    linear 0.22 alpha 0.0

transform turn_battle_impact_flash:
    alpha 0.0
    zoom 0.55
    linear 0.08 alpha 0.95 zoom 1.05
    linear 0.20 alpha 0.0 zoom 1.25

transform turn_battle_float_label:
    alpha 0.0
    yoffset 0
    linear 0.08 alpha 1.0
    linear 0.55 yoffset -24 alpha 0.0


style turn_battle_enemy_top_panel:
    background Solid("#071a36aa")
    xpos 70
    ypos 38
    xsize 470
    ysize 132
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

style turn_battle_prompt_panel:
    background Solid("#071a36a8")
    xpos 790
    ypos 252
    xsize 390
    xpadding 18
    ypadding 14

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
    xpos 1118
    ypos 210
    xsize 376
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
    xminimum 342
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

style turn_battle_action_uses is default:
    color "#f0d46b"
    insensitive_color "#788398"
    size 14
    bold True

style turn_battle_prompt_text is default:
    color "#dce7ff"
    size 16
    xalign 0.5

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

style turn_battle_freeze_beam:
    background Solid("#8fdcffcc")
    ysize 16
    xpadding 0
    ypadding 0

style turn_battle_fire_orb:
    background Solid("#ff6a2acc")
    xsize 58
    ysize 58
    xpadding 0
    ypadding 0

style turn_battle_dragon_eruption:
    background Solid("#ff3d1ecc")
    xsize 110
    ysize 92
    xpadding 0
    ypadding 0

style turn_battle_cast_label is default:
    color "#eaf4ff"
    outlines [(2, "#081022", 0, 0)]
    size 22
    bold True

style turn_battle_damage_number is default:
    color "#ffdf70"
    outlines [(2, "#230b0b", 0, 0)]
    size 30
    bold True
