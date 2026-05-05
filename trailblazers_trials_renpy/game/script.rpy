init python:
    import sys

    game_python_root = config.gamedir
    if game_python_root not in sys.path:
        sys.path.insert(0, game_python_root)

    import chapter_registry

default startup_destination = "main"

label start:

    while True:

        if startup_destination == "history":
            call screen history_menu(
                back_action=Return("back"),
                chapters_action=Return("chapter_select"),
                load_action=Return("load"),
                preferences_action=Return("preferences"),
                about_action=Return("about"),
                help_action=Return("help"),
                quit_action=Return("quit"),
            )

        elif startup_destination == "chapter_select":
            call screen chapter_select_menu(
                startup_mode=True,
                back_action=Return("back"),
                history_action=Return("history"),
                load_action=Return("load"),
                preferences_action=Return("preferences"),
                about_action=Return("about"),
                help_action=Return("help"),
                quit_action=Return("quit"),
            )

        elif startup_destination == "load":
            call screen title_load_menu(
                startup_mode=True,
                back_action=Return("back"),
                history_action=Return("history"),
                chapters_action=Return("chapter_select"),
                preferences_action=Return("preferences"),
                about_action=Return("about"),
                help_action=Return("help"),
                quit_action=Return("quit"),
            )

        elif startup_destination == "preferences":
            call screen title_preferences_menu(
                back_action=Return("back"),
                history_action=Return("history"),
                chapters_action=Return("chapter_select"),
                load_action=Return("load"),
                about_action=Return("about"),
                help_action=Return("help"),
                quit_action=Return("quit"),
            )

        elif startup_destination == "about":
            call screen about_menu(
                back_action=Return("back"),
                history_action=Return("history"),
                chapters_action=Return("chapter_select"),
                load_action=Return("load"),
                preferences_action=Return("preferences"),
                help_action=Return("help"),
                quit_action=Return("quit"),
            )

        elif startup_destination == "help":
            call screen help_menu(
                back_action=Return("back"),
                history_action=Return("history"),
                chapters_action=Return("chapter_select"),
                load_action=Return("load"),
                preferences_action=Return("preferences"),
                about_action=Return("about"),
                quit_action=Return("quit"),
            )

        elif startup_destination == "quit":
            call screen quit_confirm_menu(
                back_action=Return("back"),
                confirm_action=Return("confirm_quit"),
                history_action=Return("history"),
                chapters_action=Return("chapter_select"),
                load_action=Return("load"),
                preferences_action=Return("preferences"),
                about_action=Return("about"),
                help_action=Return("help"),
            )
        else:
            call screen startup_main_menu

        if _return in chapter_registry.playable_label_set():
            call expression _return
            return
        elif _return == "confirm_quit":
            $ renpy.quit()
        elif _return in {"history", "chapter_select", "load", "preferences", "about", "help", "quit"}:
            $ startup_destination = _return
        else:
            $ startup_destination = "main"
