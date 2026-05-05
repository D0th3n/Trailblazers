label simple_battle_preview:

    scene bg nairn fields
    with fade

    show moglim neutral at enemy_center
    with dissolve

    system "Encounter: Moglim."
    system "Small rock-based creatures with heated shells. Low threat alone, dangerous in groups."

    menu:
        "Strike carefully with squire training.":
            $ oren_resolve += 1
            $ chapter_01_result = "restrained"

            oren "Low stance. Short swing. No wasted motion."
            enemy "The Moglim rolls, hops, and launches itself across the srag like a living meteor."

        "Let the voice answer.":
            $ dragon_pressure += 2
            $ qana_strain += 1
            $ chapter_01_result = "voice"

            inner_voice "Finally."
            story "White heat crawled through Oren's veins."
            enemy "The Moglim's heated shell cracked before the sword reached it."

        "Hold back and watch how it moves.":
            $ embrum_trust += 1
            $ village_reputation += 1
            $ chapter_01_result = "studied"

            oren "It is not hunting. It is following Qana heat under the dry patches."
            enemy "The Moglim skidded sideways when Oren knocked it away from the brittle srag."

    hide moglim
    with dissolve

    return
