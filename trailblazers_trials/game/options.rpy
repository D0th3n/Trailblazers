define config.name = _("Trailblazers Trials")
define config.version = "0.1.1"
define config.window_title = _("Trailblazers Trials Prototype")
define config.save_directory = "trailblazers-trials-prototype"

define build.name = "TrailblazersTrials"
define build.version = "0.1.1"
define build.directory_name = "TrailblazersTrials-0.1.1"
define build.executable_name = "Trailblazers Trials"
define build.display_name = "Trailblazers Trials"

define config.has_sound = True
define config.has_music = True
define config.has_voice = False

define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.intra_transition = dissolve

define config.after_load_transition = fade
define config.end_game_transition = fade

define config.window = "auto"
define config.check_conflicting_properties = True

init python:
    build.classify("docs/**", None)
    build.classify("tests/**", None)
    build.classify("game/data/source_context/**", None)
    build.classify("game/images/references/**", None)
    build.classify("**/.DS_Store", None)
    build.classify("log.txt", None)
