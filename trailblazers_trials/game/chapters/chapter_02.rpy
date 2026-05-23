label chapter_02:

    $ chapter_02_result = "preparing"

    play music chapter_02_getting_ready fadeout 1.0 fadein 1.0

    scene cg chapter_02_oren_waking
    with fade

    story "Oren sat up before the inn bell finished its first ring."
    story "Gold morning pushed through the room in hard lines, catching on dust, wood grain, and the travel bag he had packed twice already."
    story "For a moment he stayed still and listened to the village waking beyond the walls."

    oren focused "One more assignment. One more chance not to become the thing they are afraid of."

    inner_voice "They are afraid because they have sense."

    oren annoyed "That was not encouragement."

    story "The room smelled like candle smoke, cold water, and iron polish. On the chair waited the red cloth Embrum insisted he wear beneath the armor."
    story "Oren looked toward the door. No footsteps yet. No summons. Just the bell, the light, and the promise that waiting would not make him readier."

    jump chapter_02_armoring


label chapter_02_checkpoint_evening:

    play music chapter_02_getting_ready fadeout 1.0 fadein 1.0

    jump chapter_02_armoring


label chapter_02_checkpoint_mine:

    play music chapter_02_hallway_walkout fadeout 1.0 fadein 1.0

    jump chapter_02_hallway


label chapter_02_armoring:

    scene cg chapter_02_oren_armoring
    with fade

    story "The armor waited across the blanket like a promise he had not agreed to keep."
    story "Black plates. Gold trim. Red cloth. Too ceremonial for a squire, too heavy for a boy who still woke expecting school bells instead of orders."

    oren focused "Left strap first. Knee guard after. Do not rush the buckles."

    story "He spoke the steps aloud because Embrum had taught him that panic hated sequence."
    story "Greave, strap, latch. Glove, clasp, breath. Each piece made him less like the person who had opened his eyes and more like someone the hallway would expect to obey."

    inner_voice "Armor is only another cage."

    oren confident "Then today I use the cage."

    story "The last clasp snapped shut. Oren flexed his fingers and watched the gauntlet answer as if it had always belonged there."

    jump chapter_02_hallway


label chapter_02_hallway:

    play music chapter_02_hallway_walkout fadeout 1.0 fadein 1.0

    scene cg chapter_02_oren_hallway
    with fade

    story "By the time Oren opened the door, the inn corridor had filled with low voices and lamp smoke."
    story "Two men at the far end stopped talking when they saw him. They tried to look away politely. They were not quick enough."

    oren neutral "Good morning."

    story "The words came out even. That felt like a small victory."
    story "Behind him, the room still held the shape of sleep: the bed unmade, the candle spent, the window bright. Ahead waited duty, questions, and whatever Embrum had decided he was ready to survive."

    inner_voice "Walk, then. Let them stare."

    story "Oren stepped into the hall and let the door close behind him."

    $ chapter_02_result = "ready"

    stop music fadeout 1.0

    call screen chapter_complete_menu(
        chapter_number="Chapter II",
        chapter_title="Oren Gets Ready",
        chapter_location="Highguard Inn",
        chapter_summary="Oren wakes, arms himself, and steps into the morning ready for the next mission placeholder.",
        chapter_status="Placeholder complete",
        replay_action=Return("replay"),
        chapters_action=Return("chapter_select"),
        title_action=Return("title"),
    )

    if _return == "replay":
        jump chapter_02
    elif _return == "chapter_select":
        $ startup_destination = "chapter_select"
        jump start
    else:
        $ startup_destination = "main"
        jump start
