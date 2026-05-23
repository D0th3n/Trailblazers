init -10 python:
    import chapter_registry
    from menu_support import WORLD_HISTORY_OVERVIEW, submit_issue_report
    import renpy.store as store

    def submit_issue_report_from_store():
        subject = store.issue_report_subject.strip() or "Untitled issue report"
        details = store.issue_report_body.strip()

        if not details:
            store.issue_report_status = "Please describe the issue before submitting."
            return

        report_path = submit_issue_report(
            config.gamedir,
            subject,
            details,
            player_name=store.issue_report_name.strip(),
        )

        store.issue_report_name = ""
        store.issue_report_subject = ""
        store.issue_report_body = ""
        store.issue_report_status = "Issue report saved to %s" % report_path

    def featured_chapter():
        return chapter_registry.featured_chapter()

    def chapter_card_entries():
        return chapter_registry.chapter_card_entries()

    def checkpoint_entries():
        return chapter_registry.checkpoint_entries()

init -9 python:
    TB_SCREEN_W = 1600
    TB_SCREEN_H = 900
    TB_NAV_W = 360
    TB_SURFACE_W = 1120
    TB_SURFACE_H = 760
    TB_SURFACE_X = TB_NAV_W + ((TB_SCREEN_W - TB_NAV_W - TB_SURFACE_W) // 2)
    TB_SURFACE_Y = (TB_SCREEN_H - TB_SURFACE_H) // 2
    TB_CARD_W = 980
    TB_CARD_H = 280
    TB_TEXT_MAX = 900


screen navigation(
    title_mode=False,
    start_action=None,
    history_action=None,
    chapters_action=None,
    load_action=None,
    preferences_action=None,
    about_action=None,
    help_action=None,
    quit_action=None,
):

    $ featured = featured_chapter()

    frame:
        style "tb_nav_panel"

        vbox:
            style "tb_nav_vbox"

            text "[config.name!t]":
                style "tb_nav_brand"

            text "Prototype":
                style "tb_nav_subbrand"

            null height 28

            if title_mode:
                if history_action is not None:
                    textbutton _("History") action history_action
                if chapters_action is not None:
                    textbutton _("Chapters") action chapters_action
                if load_action is not None:
                    textbutton _("Load") action load_action
                if preferences_action is not None:
                    textbutton _("Preferences") action preferences_action
                if about_action is not None:
                    textbutton _("About") action about_action
                if help_action is not None:
                    textbutton _("Help") action help_action
                if quit_action is not None:
                    textbutton _("Quit") action quit_action
            else:
                if start_action is not None:
                    textbutton _("Start") action start_action

                textbutton _("History") action ShowMenu("history")
                textbutton _("Save") action ShowMenu("save")
                textbutton _("Load") action ShowMenu("load")
                textbutton _("Preferences") action ShowMenu("preferences")

                if _in_replay:
                    textbutton _("End Replay") action EndReplay(confirm=True)
                else:
                    textbutton _("Main Menu") action MainMenu()

                textbutton _("About") action ShowMenu("about")

                if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
                    textbutton _("Help") action ShowMenu("help")

                if renpy.variant("pc"):
                    textbutton _("Quit") action Quit(confirm=True)

            null height 22

            text "[featured['roman']]: [featured['title']]":
                style "tb_nav_footer"


screen title_preview_panel():

    $ featured = featured_chapter()

    frame:
        style "tb_preview_outer"

        fixed:
            add Transform("menu title background", xysize=(TB_SURFACE_W, TB_SURFACE_H), alpha=0.92)
            add Solid("#09070f2c")
            add Transform("menu title logo", zoom=0.58, xalign=0.52, yalign=0.30)
            add Solid("#05060a70") xpos 0 ypos (TB_SURFACE_H - 210) xsize TB_SURFACE_W ysize 210

            vbox:
                xpos 48
                yalign 1.0
                yoffset -46
                spacing 8

                text "[featured['roman']]: [featured['title']]":
                    style "tb_preview_title"

                text "Narrative RPG Prototype":
                    style "tb_preview_subtitle"

                text "[featured['tagline']]":
                    style "tb_preview_tagline"


screen title_shell():

    add Transform("menu title background", xysize=(TB_SCREEN_W, TB_SCREEN_H))
    add Solid("#05050b60")

    text "[config.name!t]":
        style "tb_menu_window_title"


screen main_menu():

    tag menu

    use title_shell
    use navigation(
        title_mode=True,
        history_action=ShowMenu("history_menu"),
        chapters_action=ShowMenu("chapter_select_menu"),
        load_action=ShowMenu("title_load_menu"),
        preferences_action=ShowMenu("title_preferences_menu"),
        about_action=ShowMenu("about_menu"),
        help_action=ShowMenu("help_menu"),
        quit_action=ShowMenu("quit_confirm_menu"),
    )
    use title_preview_panel


screen startup_main_menu():

    tag menu

    use title_shell
    use navigation(
        title_mode=True,
        history_action=Return("history"),
        chapters_action=Return("chapter_select"),
        load_action=Return("load"),
        preferences_action=Return("preferences"),
        about_action=Return("about"),
        help_action=Return("help"),
        quit_action=Return("quit"),
    )
    use title_preview_panel


screen history_menu(
    back_action=ShowMenu("main_menu"),
    chapters_action=ShowMenu("chapter_select_menu"),
    load_action=ShowMenu("title_load_menu"),
    preferences_action=ShowMenu("title_preferences_menu"),
    about_action=ShowMenu("about_menu"),
    help_action=ShowMenu("help_menu"),
    quit_action=ShowMenu("quit_confirm_menu"),
):

    tag menu

    $ featured = featured_chapter()

    use title_shell
    use navigation(
        title_mode=True,
        history_action=NullAction(),
        chapters_action=chapters_action,
        load_action=load_action,
        preferences_action=preferences_action,
        about_action=about_action,
        help_action=help_action,
        quit_action=quit_action,
    )

    frame:
        style "tb_content_panel"

        vbox:
            spacing 18

            text "History":
                style "tb_content_title"

            text "A narrator's overview of the world before [featured['title']].":
                color "#efe4d5"
                size 18

            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"

                side_yfill True

                text WORLD_HISTORY_OVERVIEW:
                    color "#f3ebe3"
                    size 21
                    line_spacing 6
                    xmaximum TB_TEXT_MAX

    textbutton _("Back"):
        style "tb_back_button"
        action back_action


screen chapter_select_menu(
    startup_mode=False,
    back_action=ShowMenu("main_menu"),
    history_action=ShowMenu("history_menu"),
    load_action=ShowMenu("title_load_menu"),
    preferences_action=ShowMenu("title_preferences_menu"),
    about_action=ShowMenu("about_menu"),
    help_action=ShowMenu("help_menu"),
    quit_action=ShowMenu("quit_confirm_menu"),
):

    tag menu

    $ chapters = chapter_card_entries()

    use title_shell
    use navigation(
        title_mode=True,
        history_action=history_action,
        chapters_action=NullAction(),
        load_action=load_action,
        preferences_action=preferences_action,
        about_action=about_action,
        help_action=help_action,
        quit_action=quit_action,
    )

    frame:
        style "tb_content_panel"

        vbox:
            spacing 24

            text "Chapters":
                style "tb_content_title"

            text "Choose the chapter you want to begin playing right now.":
                color "#efe4d5"
                size 18

            viewport:
                id "chapter_select_scroll"
                mousewheel True
                draggable True
                pagekeys True
                scrollbars "vertical"
                xsize TB_CARD_W
                ysize 560
                child_size (TB_CARD_W, max(560, len(chapters) * (TB_CARD_H + 24)))

                side_yfill True

                vbox:
                    xsize TB_CARD_W
                    spacing 24

                    for chapter in chapters:
                        $ chapter_action = Return(chapter["start_label"]) if startup_mode else Start(chapter["start_label"])
                        button:
                            style "tb_chapter_card_button"
                            action chapter_action

                            fixed:
                                add Transform(chapter["menu_background"], xysize=(760, 220))
                                add Solid("#140d09a0")

                                vbox:
                                    xpos 28
                                    ypos 26
                                    spacing 6

                                    text "[chapter['number']]":
                                        style "tb_chapter_label"

                                    text "[chapter['title']]":
                                        style "tb_chapter_title"

                                    text "[chapter['location']]":
                                        style "tb_chapter_location"

                                    text "[chapter['summary']]":
                                        style "tb_chapter_summary"

            text "More chapters will unlock here as Trailblazers Trials expands.":
                color "#c8b8a4"
                size 16

    textbutton _("Back"):
        style "tb_back_button"
        action back_action


screen title_load_menu(
    startup_mode=False,
    back_action=ShowMenu("main_menu"),
    history_action=ShowMenu("history_menu"),
    chapters_action=ShowMenu("chapter_select_menu"),
    preferences_action=ShowMenu("title_preferences_menu"),
    about_action=ShowMenu("about_menu"),
    help_action=ShowMenu("help_menu"),
    quit_action=ShowMenu("quit_confirm_menu"),
):

    tag menu

    $ checkpoints = checkpoint_entries()

    use title_shell
    use navigation(
        title_mode=True,
        history_action=history_action,
        chapters_action=chapters_action,
        load_action=NullAction(),
        preferences_action=preferences_action,
        about_action=about_action,
        help_action=help_action,
        quit_action=quit_action,
    )

    frame:
        style "tb_content_panel"

        vbox:
            spacing 20

            text "Load":
                style "tb_content_title"

            text "Jump into an available chapter from a later checkpoint instead of always starting from the opening recap.":
                color "#efe4d5"
                size 18

            for checkpoint in checkpoints:
                $ checkpoint_action = Return(checkpoint["label"]) if startup_mode else Start(checkpoint["label"])
                textbutton "[checkpoint['chapter_number']]: [checkpoint['chapter_title']] - [checkpoint['menu_label']]":
                    style "tb_load_button"
                    action checkpoint_action

            text "These are chapter checkpoints. In-game save slots still become useful once you create your own saves during play.":
                color "#c8b8a4"
                size 16
                xmaximum TB_TEXT_MAX

    textbutton _("Back"):
        style "tb_back_button"
        action back_action


screen title_preferences_menu(
    back_action=ShowMenu("main_menu"),
    history_action=ShowMenu("history_menu"),
    chapters_action=ShowMenu("chapter_select_menu"),
    load_action=ShowMenu("title_load_menu"),
    about_action=ShowMenu("about_menu"),
    help_action=ShowMenu("help_menu"),
    quit_action=ShowMenu("quit_confirm_menu"),
):

    tag menu

    use title_shell
    use navigation(
        title_mode=True,
        history_action=history_action,
        chapters_action=chapters_action,
        load_action=load_action,
        preferences_action=NullAction(),
        about_action=about_action,
        help_action=help_action,
        quit_action=quit_action,
    )

    frame:
        style "tb_content_panel"

        vbox:
            spacing 18

            text "Preferences":
                style "tb_content_title"

            text "Control the display mode and the most important reading and audio settings.":
                color "#efe4d5"
                size 18

            hbox:
                spacing 20

                text "Screen Mode":
                    style "tb_pref_label"

                textbutton "Window":
                    style "tb_pref_choice_button"
                    action Preference("display", "window")

                textbutton "Fullscreen":
                    style "tb_pref_choice_button"
                    action Preference("display", "fullscreen")

            vbox:
                spacing 10

                text "Text Speed":
                    style "tb_pref_label"
                bar value Preference("text speed") style "tb_pref_bar"

                text "Auto-Forward Time":
                    style "tb_pref_label"
                bar value Preference("auto-forward time") style "tb_pref_bar"

                text "Music Volume":
                    style "tb_pref_label"
                bar value Preference("music volume") style "tb_pref_bar"

                text "Sound Volume":
                    style "tb_pref_label"
                bar value Preference("sound volume") style "tb_pref_bar"

                text "Voice Volume":
                    style "tb_pref_label"
                bar value Preference("voice volume") style "tb_pref_bar"

            hbox:
                spacing 20

                text "Skip":
                    style "tb_pref_label"

                textbutton "Seen Text":
                    style "tb_pref_choice_button"
                    action Preference("skip", "seen")

                textbutton "All Text":
                    style "tb_pref_choice_button"
                    action Preference("skip", "all")

    textbutton _("Back"):
        style "tb_back_button"
        action back_action


screen about_menu(
    back_action=ShowMenu("main_menu"),
    history_action=ShowMenu("history_menu"),
    chapters_action=ShowMenu("chapter_select_menu"),
    load_action=ShowMenu("title_load_menu"),
    preferences_action=ShowMenu("title_preferences_menu"),
    help_action=ShowMenu("help_menu"),
    quit_action=ShowMenu("quit_confirm_menu"),
):

    tag menu

    use title_shell
    use navigation(
        title_mode=True,
        history_action=history_action,
        chapters_action=chapters_action,
        load_action=load_action,
        preferences_action=preferences_action,
        about_action=NullAction(),
        help_action=help_action,
        quit_action=quit_action,
    )

    frame:
        style "tb_content_panel"

        vbox:
            spacing 18

            text "About":
                style "tb_content_title"

            text "Trailblazers Trials is an indie narrative RPG prototype and the first project of PecanStudios.":
                color "#f3ebe3"
                size 21
                xmaximum TB_TEXT_MAX

            text "Developed by Murks with AI-assisted production support from Codex, the project is being built chapter by chapter as a world-first lore page, VN, and hybrid exploration prototype.":
                color "#f3ebe3"
                size 19
                xmaximum TB_TEXT_MAX

            text "This build focuses on Chapter 1: Heart of Fire, using custom art, iterative worldbuilding, and AI assistance as part of an intentionally independent development pipeline.":
                color "#c8b8a4"
                size 17
                xmaximum TB_TEXT_MAX

    textbutton _("Back"):
        style "tb_back_button"
        action back_action


screen help_menu(
    back_action=ShowMenu("main_menu"),
    history_action=ShowMenu("history_menu"),
    chapters_action=ShowMenu("chapter_select_menu"),
    load_action=ShowMenu("title_load_menu"),
    preferences_action=ShowMenu("title_preferences_menu"),
    about_action=ShowMenu("about_menu"),
    quit_action=ShowMenu("quit_confirm_menu"),
):

    tag menu

    use title_shell
    use navigation(
        title_mode=True,
        history_action=history_action,
        chapters_action=chapters_action,
        load_action=load_action,
        preferences_action=preferences_action,
        about_action=about_action,
        help_action=NullAction(),
        quit_action=quit_action,
    )

    frame:
        style "tb_content_panel"

        vbox:
            spacing 16

            text "Help":
                style "tb_content_title"

            text "Use this page to report issues. Reports are saved into the project's game folder so they can be reviewed later.":
                color "#efe4d5"
                size 18
                xmaximum TB_TEXT_MAX

            text "Player Name (optional)":
                style "tb_pref_label"
            input value VariableInputValue("issue_report_name") length 48 color "#f3ebe3" size 20

            text "Short Subject":
                style "tb_pref_label"
            input value VariableInputValue("issue_report_subject") length 72 color "#f3ebe3" size 20

            text "Issue Details":
                style "tb_pref_label"
            input value VariableInputValue("issue_report_body", returnable=True) length 800 color "#f3ebe3" size 20

            hbox:
                spacing 18

                textbutton "Submit Report":
                    style "tb_pref_choice_button"
                    action Function(submit_issue_report_from_store)

                textbutton "Clear":
                    style "tb_pref_choice_button"
                    action [
                        SetVariable("issue_report_name", ""),
                        SetVariable("issue_report_subject", ""),
                        SetVariable("issue_report_body", ""),
                        SetVariable("issue_report_status", ""),
                    ]

            if issue_report_status:
                text "[issue_report_status]":
                    color "#ffd68f"
                    size 18
                    xmaximum TB_TEXT_MAX

    textbutton _("Back"):
        style "tb_back_button"
        action back_action


screen quit_confirm_menu(
    back_action=ShowMenu("main_menu"),
    confirm_action=Quit(confirm=False),
    history_action=ShowMenu("history_menu"),
    chapters_action=ShowMenu("chapter_select_menu"),
    load_action=ShowMenu("title_load_menu"),
    preferences_action=ShowMenu("title_preferences_menu"),
    about_action=ShowMenu("about_menu"),
    help_action=ShowMenu("help_menu"),
):

    tag menu

    use title_shell
    use navigation(
        title_mode=True,
        history_action=history_action,
        chapters_action=chapters_action,
        load_action=load_action,
        preferences_action=preferences_action,
        about_action=about_action,
        help_action=help_action,
        quit_action=NullAction(),
    )

    frame:
        style "tb_content_panel"

        vbox:
            spacing 24
            xalign 0.5
            yalign 0.5

            text "Do you really want to quit?":
                style "tb_content_title"
                xalign 0.5

            hbox:
                spacing 24
                xalign 0.5

                textbutton "No":
                    style "tb_pref_choice_button"
                    action back_action

                textbutton "Yes":
                    style "tb_pref_choice_button"
                    action confirm_action

    textbutton _("Back"):
        style "tb_back_button"
        action back_action


screen chapter_complete_menu(
    chapter_number="Chapter I",
    chapter_title="Heart of Fire",
    chapter_location="Anozira Village",
    chapter_summary="Anozira breathes again, but the deeper truth under Ruzen remains hidden.",
    chapter_status="Chapter complete",
    replay_action=Return("replay"),
    chapters_action=Return("chapter_select"),
    title_action=Return("title"),
):

    tag menu
    modal True

    add Transform("cg anozira thanks ending", xysize=(TB_SCREEN_W, TB_SCREEN_H))
    add Solid("#05050bb2")

    frame:
        style "tb_complete_panel"

        vbox:
            spacing 18
            xfill True

            text "[chapter_status]":
                style "tb_complete_kicker"

            text "[chapter_number]: [chapter_title]":
                style "tb_complete_title"

            text "[chapter_location]":
                style "tb_complete_location"

            text "[chapter_summary]":
                style "tb_complete_summary"

            text "Choose what you want to do next.":
                color "#efe4d5"
                size 20

            hbox:
                spacing 20

                textbutton "Replay Chapter":
                    style "tb_pref_choice_button"
                    action replay_action

                textbutton "Chapters":
                    style "tb_pref_choice_button"
                    action chapters_action

                textbutton "Title Menu":
                    style "tb_pref_choice_button"
                    action title_action


screen say(who, what):

    style_prefix "say"

    window:
        id "window"
        style "say_window"

        vbox:
            spacing 4

            if who is not None:
                text who:
                    id "who"
                    style "say_label"

            text what:
                id "what"
                style "say_dialogue"


screen choice(items):

    style_prefix "choice"

    zorder 120

    fixed:
        add Solid("#130905d8") xpos 0 ypos 0 xsize TB_SCREEN_W ysize 220

        vbox:
            style "choice_vbox"
            xpos 40
            ypos 24

            for i in items:
                textbutton i.caption action i.action


screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "tb_game"

    add Transform("menu title background", xysize=(TB_SCREEN_W, TB_SCREEN_H))
    add Solid("#05050b88")

    text "[config.name!t]":
        style "tb_menu_window_title"

    use navigation(start_action=None)

    frame:
        style "tb_content_panel"

        vbox:
            spacing 20

            text title:
                style "tb_content_title"

            if scroll == "viewport":

                viewport:
                    mousewheel True
                    draggable True
                    pagekeys True
                    scrollbars "vertical"
                    yinitial yinitial

                    side_yfill True

                    vbox:
                        spacing spacing
                        transclude

            elif scroll == "vpgrid":

                vpgrid:
                    cols 1
                    mousewheel True
                    draggable True
                    pagekeys True
                    scrollbars "vertical"
                    yinitial yinitial
                    spacing spacing

                    side_yfill True

                    transclude

            else:

                transclude

    textbutton _("Back"):
        style "tb_back_button"
        action Return()

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style tb_nav_panel is empty
style tb_nav_vbox is vbox
style tb_nav_button is button
style tb_nav_button_text is text
style tb_nav_brand is text
style tb_nav_subbrand is text
style tb_nav_footer is text
style tb_menu_window_title is text
style tb_preview_outer is empty
style tb_preview_title is text
style tb_preview_subtitle is text
style tb_preview_tagline is text
style tb_content_panel is empty
style tb_content_title is text
style tb_chapter_card_button is button
style tb_chapter_label is text
style tb_chapter_title is text
style tb_chapter_location is text
style tb_chapter_summary is text
style tb_back_button is button
style tb_back_button_text is text
style tb_load_button is button
style tb_load_button_text is text
style tb_pref_label is text
style tb_pref_choice_button is button
style tb_pref_choice_button_text is text
style tb_pref_bar is bar
style tb_complete_panel is empty
style tb_complete_kicker is text
style tb_complete_title is text
style tb_complete_location is text
style tb_complete_summary is text
style say_window is empty
style say_label is text
style say_dialogue is text
style choice_vbox is vbox
style choice_button is button
style choice_button_text is text


style tb_nav_panel:
    background Solid("#081118dc")
    xpos 0
    ypos 0
    xsize TB_NAV_W
    yfill True
    left_padding 34
    right_padding 28
    top_padding 44
    bottom_padding 36

style tb_nav_vbox:
    spacing 14
    yalign 0.5

style tb_nav_button:
    background Solid("#00000000")
    hover_background Solid("#c88b3528")
    selected_background Solid("#c88b3538")
    xfill True
    left_padding 12
    right_padding 12
    top_padding 8
    bottom_padding 8

style tb_nav_button_text:
    color "#f0e7d8"
    hover_color "#ffd68f"
    selected_color "#ffd68f"
    size 22

style tb_nav_brand:
    color "#f6efe2"
    size 26

style tb_nav_subbrand:
    color "#c8b8a4"
    size 14

style tb_nav_footer:
    color "#be9150"
    size 13

style tb_menu_window_title:
    color "#f7f2ea"
    size 18
    xalign 0.5
    yalign 0.03

style tb_preview_outer:
    background Solid("#120b10dc")
    xpos TB_SURFACE_X
    ypos TB_SURFACE_Y
    xsize TB_SURFACE_W
    ysize TB_SURFACE_H
    left_padding 0
    right_padding 0
    top_padding 0
    bottom_padding 0

style tb_preview_title:
    color "#f4b55a"
    size 34

style tb_preview_subtitle:
    color "#f1d8a5"
    size 22

style tb_preview_tagline:
    color "#d8d5ee"
    size 17

style tb_content_panel:
    background Solid("#120b10ea")
    xpos TB_SURFACE_X
    ypos TB_SURFACE_Y
    xsize TB_SURFACE_W
    ysize TB_SURFACE_H
    left_padding 34
    right_padding 34
    top_padding 28
    bottom_padding 28

style tb_content_title:
    color "#f2c267"
    size 34

style tb_chapter_card_button:
    background Solid("#120b10ee")
    hover_background Solid("#2a1511f4")
    xsize TB_CARD_W
    ysize TB_CARD_H
    left_padding 0
    right_padding 0
    top_padding 0
    bottom_padding 0

style tb_chapter_label:
    color "#ffd68f"
    size 18

style tb_chapter_title:
    color "#fff5e1"
    size 36

style tb_chapter_location:
    color "#f2c267"
    size 20

style tb_chapter_summary:
    color "#f3ebe3"
    size 16
    xmaximum 820

style tb_load_button:
    background Solid("#1a1014f0")
    hover_background Solid("#2a1511f4")
    xfill True
    left_padding 18
    right_padding 18
    top_padding 14
    bottom_padding 14

style tb_load_button_text:
    color "#f3ebe3"
    hover_color "#ffd68f"
    size 22

style tb_pref_label:
    color "#f1d8a5"
    size 19

style tb_pref_choice_button:
    background Solid("#1a1014f0")
    hover_background Solid("#2a1511f4")
    left_padding 16
    right_padding 16
    top_padding 10
    bottom_padding 10

style tb_pref_choice_button_text:
    color "#f0e7d8"
    hover_color "#ffd68f"
    size 18

style tb_pref_bar:
    xmaximum 520
    ymaximum 18
    left_bar Frame(Solid("#f2c267"), 2, 2)
    right_bar Frame(Solid("#39251a"), 2, 2)
    thumb None

style tb_complete_panel:
    background Solid("#120a08db")
    xalign 0.5
    yalign 0.5
    xsize 860
    left_padding 44
    right_padding 44
    top_padding 42
    bottom_padding 42

style tb_complete_kicker:
    color "#d9a24d"
    size 22

style tb_complete_title:
    color "#f8f1e8"
    size 46

style tb_complete_location:
    color "#d8b179"
    size 28

style tb_complete_summary:
    color "#f3ebe3"
    size 24
    xmaximum 740

style say_window:
    background Solid("#120a08d6")
    xpos 20
    ypos 18
    xmaximum 1140
    left_padding 18
    right_padding 18
    top_padding 10
    bottom_padding 12

style say_label:
    color "#d8c4a4"
    size 24

style say_dialogue:
    color "#fff7ee"
    size 28
    line_spacing 3
    xmaximum 1080

style choice_vbox:
    spacing 10

style choice_button:
    background Solid("#00000000")
    hover_background Solid("#f4b55a28")
    xmaximum 1480
    left_padding 0
    right_padding 0
    top_padding 0
    bottom_padding 0

style choice_button_text:
    color "#fff7ee"
    hover_color "#ffd68f"
    size 34
    text_align 0.0
    xalign 0.0

style tb_back_button:
    background Solid("#081118dc")
    hover_background Solid("#c88b3528")
    xpos 34
    yalign 1.0
    yoffset -30
    left_padding 18
    right_padding 18
    top_padding 10
    bottom_padding 10

style tb_back_button_text:
    color "#f0e7d8"
    hover_color "#ffd68f"
    size 20
