label chapter_02:

    scene bg severance dark
    with fade

    story "Several months after the Dravrah Incident, the kingdom chose surveillance over execution."
    story "Oren had saved an academy. He had also shown enough power to make every witness afraid of what came after saving."
    story "Master Embrum was given two orders: watch the young squire, and answer a village drought the court had waited too long to touch."
    story "By sunrise, Anozira would become Oren's first field test under Highguard eyes."

    scene bg village dawn
    with fade

    story "Dawn came pale over Anozira Village."
    story "The srag along the road had dried into brittle curls, and the nairn rows beyond the fence leaned like tired soldiers."
    story "Anozira's nairn usually fed Brumel herds across the sea, but now even the Port of Eldran had begun sending worried riders."
    story "Even the CAC-approved Qana recycler clicked without rhythm, pulling heat from the air while the wells gave back only warmth and steam."

    show oren neutral at portrait_left
    with dissolve

    story "Every kindness still felt like a guardrail."
    story "Embrum brought Oren because his orders were simpler than kindness: keep the boy close, watch his Qana output, and do not let Dravrah happen twice."
    story "Oren woke with dust on his tongue and a thought in his chest that did not feel like thought."

    inner_voice "This cage is too small."

    oren "Not now."

    inner_voice "I am Jötunn. I was not born to crawl in a boy's heart."

    $ heard_jotunn_claim = True

    oren "Dragons were sealed two thousand years ago. That is not real."

    show guard neutral at portrait_right
    with dissolve

    guard "Squire Oren? Master Embrum wants you near the north fields. Highguard orders say you are not to move alone."

    menu:
        "Admit you heard something strange.":
            $ village_reputation += 1
            $ dragon_pressure += 1
            $ saw_inner_dragon = True

            oren "I heard something. A voice. Maybe mine. Maybe not."

            guard "The drought is making everyone hear things. Last night Mistress Vale swore the Highest Order whispered from her empty well."
            guard "This morning an Eldran merchant claimed the royal blood would not let Anozira fail."

        "Hide the voice and act normal.":
            $ oren_resolve += 1
            $ chose_to_hide_dragon = True

            oren "Bad dream. Nothing more."

            guard "Then wake up fast. The village cannot spare another pair of useless hands, not while the nairn carts sit empty."

    hide guard
    with dissolve

    show embrum neutral at portrait_right
    with dissolve

    embrum "There you are."

    oren "Master Embrum."

    embrum "The Highguard chief called Anozira a small village matter. That usually means the kingdom wants it solved without admitting it waited too long."
    embrum "The north srag fields are failing. Nairn is failing, sinu is wilting, and people are starting to call this punishment."
    embrum "Eldran exporters are already counting lost shipments."

    menu:
        "Tell Embrum the voice called itself Jötunn.":
            $ embrum_trust += 1
            $ chose_to_trust_embrum = True

            oren "The voice gave me a name. Jötunn."

            embrum "A name from your own mouth can still frighten you."

            oren "You think I made it up."

            embrum "I think the kingdom put you under my watch because your Qana output can outrun your judgment."
            embrum "At Dravrah, you destroyed the creature and part of the school with it. Here, you control your output before anger controls it for you."

        "Ask if the drought could be divine punishment.":
            $ village_reputation += 1

            oren "People keep saying the Highest Order is testing us."

            embrum "People say that when the royal family is far away, the wells are empty, and the Port of Eldran wants answers."

            inner_voice "Small prayers. Smaller answers."

        "Push the voice down and focus on the crisis.":
            $ qana_strain += 1
            $ dragon_pressure -= 1

            oren "The fields first. My head can wait."

            embrum "Good. Anozira needs hands more than panic. And you need control more than excuses."

    story "Embrum sent Oren ahead through the square instead of straight to the mayor."
    story "Listen first, he said. A village tells the truth in the spaces between its speeches."

    call chapter_02_anozira_square_exploration

    scene bg village square
    with fade

    show prop empty_nairn_cart at prop_right
    show mayor neutral at portrait_left
    show embrum neutral at portrait_right
    with dissolve

    story "Anozira's market should have been loud with nairn ledgers, feed arguments, and Port of Eldran bargaining."
    story "Instead it felt half-emptied by heat, with more worry than trade gathered between the stalls."

    mayor "Master Embrum, the north path is crawling with Moglim again. Wherever they pass, the srag dries white."
    mayor "If this reaches another tenday, Anozira will have no nairn for Brumel, no sinu for our own kitchens, and no answer for Eldran."

    hide mayor
    show villager neutral at portrait_left
    with dissolve

    villager "They are worse near the ditch stones, where the srag should still hold a little damp."
    villager "My brother tried to drive them off before sunrise. Said they rolled like hot stones and left the srag smoking behind them."

    embrum "Moglim near nairn fields usually means a Qana disturbance nearby. Not a curse until proven otherwise."

    hide villager
    show eldran merchant neutral at portrait_left
    with dissolve

    eldran_merchant "Not a curse, not a shipment, not my concern what name you give it. The Port of Eldran is counting empty carts."
    eldran_merchant "If word reaches the capital, the royal blood may yet save you. Or the Highest Order may remember you first."

    embrum "If word reaches the capital, it will arrive slower than thirst."

    oren "So we go now."

    call simple_battle_preview

    scene bg village square
    with fade

    show prop empty_nairn_cart at prop_right
    show prop defeated_moglim at prop_evidence
    show oren neutral at portrait_left
    show embrum neutral at portrait_right
    with dissolve

    if chapter_02_result == "restrained":
        embrum "Good. You kept your fear from choosing for you."
        inner_voice "He praises weakness because he has never remembered wings."
    elif chapter_02_result == "voice":
        embrum "That was too much output, Oren."
        embrum "If you lose control here like you did at Dravrah, I will stop you before the village pays for it."
        inner_voice "At last. You listened."
    else:
        embrum "You watched first. That may tell us more than a clean strike would have."

    story "They returned with scorched Moglim remains wrapped in torn cloth and ash from the north srag still clinging to their boots."
    story "The creatures had not been wandering. They had gathered where the soil held heat like a buried stove."

    hide oren
    show mayor neutral at portrait_left
    with dissolve

    mayor "Tell me there is an answer in those stones."

    embrum "There is a lead. Not an answer."
    embrum "Your Qana recycler is working. That is what concerns me."

    mayor "Working?"

    embrum "It is fighting the air, but your problem is under the ground."
    embrum "If the reservoirs beneath Anozira are heating, your wells will steam empty no matter how clean the air is."

    mayor "Then you mean the Ruzen mines."

    embrum "Why would I mean the mines?"

    mayor "Ruzen is our second-most valuable export after nairn. Or it was."
    mayor "The mines shut down three weeks ago, but not from a cave-in. First the heat got strange. Then the seams glowed at night."
    mayor "Then the wells nearest the mine ridge started coughing steam."

    inner_voice "Something is drinking the mountain."

    hide mayor
    show oren neutral at portrait_left
    with dissolve

    oren "Steam from wells?"

    hide oren
    show mayor neutral at portrait_left
    with dissolve

    mayor "Warm water first. Then less water. Now some buckets come up dry enough to burn the rope."

    embrum "The mine heat started before the wells failed?"

    mayor "No, Master Embrum. The storms are why it shut down."
    mayor "Sudden heat bursts. Fire turning in the air like rope. Cracks opening bright enough to see through stone."
    mayor "Tools became too hot to hold."

    inner_voice "This is not how stone warms on its own."

    hide mayor
    show oren neutral at portrait_left
    with dissolve

    oren "Not now."

    embrum "We do not assume a monster. We assume a source."
    embrum "If something below Ruzen is heating the reservoirs, the Moglim are only scavengers drawn to the warmth."

    $ chapter_02_ruzen_lead_unlocked = True

    story "Anozira still had no answer for its drought."
    story "But it had its first honest lead: scorched srag, hungry Moglim, steaming wells, and a mine hot enough to empty the earth below it."
    story "Oren could not decide whether the voice inside him was madness or memory, only that it recognized the hunger in the heat before anyone else did."

    call chapter_02_anozira_evening_interlude

    call chapter_02_ruzen_mine_approach

    return

label chapter_02_checkpoint_evening:

    $ chapter_02_visited_village_exploration = True
    $ chapter_02_village_square_exploration_complete = True
    $ chapter_02_explored_village_well = True
    $ chapter_02_explored_village_rumor = True
    $ chapter_02_ruzen_lead_unlocked = True
    $ chapter_02_result = "restrained"

    call chapter_02_anozira_evening_interlude
    call chapter_02_ruzen_mine_approach

    return

label chapter_02_checkpoint_mine:

    $ chapter_02_visited_village_exploration = True
    $ chapter_02_village_square_exploration_complete = True
    $ chapter_02_explored_village_well = True
    $ chapter_02_explored_village_rumor = True
    $ chapter_02_visited_tavern = True
    $ chapter_02_ruzen_lead_unlocked = True
    $ chapter_02_heard_dead_miner_hint = True
    $ chapter_02_result = "restrained"

    call chapter_02_ruzen_mine_approach

    return

label chapter_02_anozira_square_exploration:

    $ chapter_02_visited_village_exploration = True
    $ chapter_02_village_square_exploration_complete = False
    $ exploration_begin("chapter_02_anozira_square", reset_position=True)

    while not chapter_02_village_square_exploration_complete:
        scene bg anozira exploration
        call screen exploration_screen

        if _return == "well":
            if not chapter_02_explored_village_well:
                $ chapter_02_explored_village_well = True

                scene bg village square
                with dissolve

                show oren neutral at portrait_left
                with dissolve

                story "Steam leaked from the well in weak white breaths."
                oren "The rope is dry, but the stones are sweating."
                oren "If the water below is this hot, the ground under the fields has to be worse."
                inner_voice "Something below is feeding. The earth is only the skin of it."
            else:
                story "The same hot breath hissed from the well stones. Whatever heated the reservoirs had not eased."

        elif _return == "villager":
            if not chapter_02_explored_village_rumor:
                $ chapter_02_explored_village_rumor = True
                $ village_reputation += 1

                scene bg village square
                with dissolve

                show villager neutral at portrait_left
                show oren neutral at portrait_right
                with dissolve

                villager "You feel it too, don't you? The ditch stones keep their heat even before sunrise."
                villager "Moglim do not roll there by accident anymore. They wait near the warm ground like they know something under us is waking."
                oren "Toward the mine ridge?"
                villager "Toward the wells first. Then the ridge."
            else:
                story "The villager had nothing new, only the same fear: warm stones, watchful Moglim, and a village pretending the wells might still recover on their own."

        elif _return == "market_exit":
            $ chapter_02_village_square_exploration_complete = True

            scene bg village square
            with dissolve

            story "Oren crossed into the market edge where two half-empty stalls and a ruined nairn cart marked how much trade the drought had already stolen."
            story "Embrum waited there with Mayor Vale, using the market square itself as a meeting ground so every anxious villager could hear what came next."

        $ exploration_result = None

    return

label chapter_02_anozira_evening_interlude:

    scene bg tavern night
    with fade

    show oren neutral at portrait_left
    show embrum neutral at portrait_right
    with dissolve

    story "Embrum did not take Oren to the mines that night."
    story "Instead, he took him where frightened villages always gathered after sunset: near firelight, cheap drink, and people pretending not to listen."

    $ chapter_02_visited_tavern = True

    embrum "Before we step into Ruzen, we learn what the miners refused to say in front of the mayor."

    hide oren
    show drunk_father neutral at portrait_left
    with dissolve

    drunk_father "Ruzen takes sons. Always did. But it used to give the bodies back."

    embrum "You lost someone there?"

    drunk_father "My boy. Brann."
    drunk_father "Good hands. Strong back. Thought he could outrun a heat burst because every young fool thinks the world owes him one more breath."

    oren "Was his body recovered?"

    drunk_father "No."
    drunk_father "They sealed the lower drift before the smoke cleared. Said another rescue would cost three more lives."
    drunk_father "So I drink for a grave I cannot visit."

    inner_voice "Hot earth does not forget what it keeps."

    oren "I am sorry."

    drunk_father "Sorry is for the living, squire."

    $ chapter_02_heard_dead_miner_hint = True

    hide drunk_father
    show wounded_miner neutral at portrait_left
    with dissolve

    wounded_miner "If you go to Ruzen, do not trust the quiet."

    embrum "You were inside when it changed?"

    wounded_miner "Close enough."
    wounded_miner "Fire came sideways down the lower drift. Not up, not forward. Sideways."
    wounded_miner "The foreman calls it pressure in the walls. I call it a furnace learning how to wake."

    story "By the time Embrum led Oren back toward the square, the miner's warning had already spread ahead of them like smoke."
    story "If even the quiet inside Ruzen could not be trusted, then the roads and wells above it had no reason to feel safe."

    scene bg village square night
    with fade

    show water_worker neutral at portrait_left
    show oren neutral at portrait_right
    with dissolve

    story "Night settled over Anozira. The recycler glowed blue in the square while the stones around the well held the day's heat like banked coals."

    water_worker "We pulled water until the handles cracked."
    water_worker "Then the buckets came up warm. Then they came up hissing."

    oren "From the well?"

    water_worker "From every well that still answers. Half of them spit steam before they give a cup."
    water_worker "And the water that does come up tastes like the mountain is chewing on the iron below us."

    story "A woman and her daughter crossed the square with an empty clay jug between them."

    hide oren
    show village_woman neutral at portrait_right
    with dissolve

    village_woman "Please. Just enough to get her through the night."

    water_worker "I cannot."
    water_worker "Every barrel that came in was counted before the cart wheels stopped. Sold, marked, or promised."

    village_woman "She is a child."

    water_worker "I know."
    water_worker "And if I break the count for one child, twenty more mothers will be here before moonset with empty hands."

    hide water_worker
    show village_daughter neutral at portrait_left
    with dissolve

    village_daughter "I tried the well before we came."

    oren "Was it hot?"

    village_daughter "It was looking back."
    village_daughter "Little red flickers under the water stones. Like Moglim eyes."

    inner_voice "Below. Not beside."

    hide village_woman
    hide village_daughter
    show oren neutral at portrait_left
    show embrum neutral at portrait_right
    with dissolve

    oren "The Moglim are underneath the village."

    embrum "Or the heat is driving them toward every hollow that still holds Qana."

    embrum "We go at first light."

    oren "Not tonight?"

    embrum "Not blind, not tired, and not because a frightened village needs us to hurry."

    inner_voice "Delay changes nothing. The mountain is already feeding."

    story "Oren slept badly, if he slept at all."

    return

label chapter_02_ruzen_mine_approach:

    scene bg ruzen mine entrance
    with fade

    show miner_foreman neutral at portrait_left
    show embrum neutral at portrait_right
    with dissolve

    story "By first light, the path out of Anozira had turned from brittle srag to black stone and Ruzen dust."
    story "The mine entrance sagged under cracked beams. A hand-painted sign warned the stubborn away: closed, unsafe, keep out."

    foreman "If the mayor sent you to open those tunnels, tell him no amount of nairn debt is worth cooking men alive."

    embrum "We are not reopening the mine."
    embrum "We are finding out why your mountain is cooking the wells dry."

    foreman "Then start with what changed."
    foreman "Ruzen has always been dangerous. Fire-Qana weather builds in the deep seams. You learn the signs or you die."

    oren "Fire-Qana weather?"

    foreman "Flame lashes. Heat pockets. Sometimes a twist of fire if Qana sits too long in one shaft."
    foreman "We got confident. Maybe too confident. We knew when to back away."
    foreman "Then two or three months ago, the whole mountain started getting hotter."

    hide miner_foreman
    show miner neutral at portrait_left
    with dissolve

    miner "Foreman wanted bigger Ruzen crystals before the Eldran shipment."
    miner "Said if we met quota early, there'd be coin enough for everyone."

    hide miner
    show miner_foreman neutral at portrait_left
    with dissolve

    foreman "I said it. I own it."
    foreman "We went deeper than we should have. Qana built too fast, the flames twisted into columns, and the drift boxed us in."

    hide miner_foreman
    show miner neutral at portrait_left
    with dissolve

    miner "Most of us crawled out."
    miner "Two didn't."
    miner "Brann had his father waiting at the tavern."
    miner "The other had his mother and little sister waiting near the well road."

    hide miner
    show miner_foreman neutral at portrait_left
    with dissolve

    foreman "Their bodies were lost to the flames."
    foreman "After that, people started saying the wells turned against us because we left village boys under the mountain."

    embrum "The water changed after the expedition?"

    foreman "First it came up hot. Then boiling."
    foreman "Then it burned off before it reached the bucket."
    foreman "We requested emergency water barrels from the nearest city three months ago. First shipment only just rolled in."
    foreman "No one knows when the next one comes."

    hide miner_foreman
    show miner neutral at portrait_left
    with dissolve

    miner "You two stand there like the air is only warm."
    miner "Men gag trying to breathe inside. How are you fine?"

    embrum "Fire-Qana users can draw from dense heat if they know how to filter it."
    embrum "To you, it is a furnace. To us, it is a dangerous refill."

    inner_voice "The air is rich. Drink."

    story "Oren flinched before he could stop himself."

    embrum "Oren?"

    oren "Nothing. The mine."

    scene bg ruzen deep passage
    with fade

    show oren neutral at portrait_left
    show embrum neutral at portrait_right
    with dissolve

    story "Inside, the deeper passage pulsed with dull red crystal light. Heat gathered in waves, then vanished, then returned sharp enough to sting the eyes."

    embrum "Deep Ruzen seams over lava could explain heat."
    embrum "But not this steady rise, and not every reservoir failing at once."

    story "A line of cracked crystal ran along the wall, too straight to be natural and too fresh to be old mining damage."

    inner_voice "Something is feeding on the stone."

    oren "There are cuts in the wall."

    embrum "I see them."
    embrum "And I do not like how clean they are."

    $ chapter_02_mine_tampering_suspected = True

    story "They pressed deeper."
    story "The Qana grew thick enough that Oren could feel it before he saw where the tunnels turned."
    story "It had a scent without smell: hot metal, old ash, and something vast pulling breath through stone."

    inner_voice "Left."

    oren "Left."

    embrum "You can feel it too."

    oren "Almost smell it."

    embrum "High-density Qana does that to trained senses. Do not trust it blindly. Follow it carefully."

    show moglim mogul at mogul_center
    with dissolve

    story "The first Moglim came alone, its shell glowing like banked coal."
    story "Then three more rolled out from a side crack."
    story "Then the tunnel floor rattled with many hidden legs."

    embrum "Careful. I saw Moglim nearby."
    embrum "No, more than nearby. That is a whole Mogul."

    $ chapter_02_mogul_encountered = True

    menu:
        "Cut a path through the Mogul.":
            $ oren_resolve += 1
            $ qana_strain += 1

            oren "Short strikes. Keep them from rolling together."
            story "Oren broke the first heated shell, then used the recoil to knock the next two away from Embrum's flank."

        "Let the fire-Qana refill you before striking.":
            $ dragon_pressure += 1
            $ qana_strain = max(qana_strain - 1, 0)

            inner_voice "Now you understand. The furnace can feed you."
            story "Oren inhaled heat that should have burned his throat. Instead, it filled the hollow places in his Qana pools."
            story "His spear moved like a streak of red-white light through the Mogul."

        "Hold formation with Embrum.":
            $ embrum_trust += 1

            embrum "Back to back."
            oren "I have your left."
            story "The Moglim bounced and rolled, but neither man gave them a gap wide enough to break through."

    hide moglim
    with dissolve

    scene bg ruzen fire tornado passage
    with fade

    show oren neutral at portrait_left
    show embrum neutral at portrait_right
    with dissolve

    story "Past the Mogul, fire tornadoes crawled across the lower passage."
    story "The columns twisted from floor to ceiling, fed by Qana weather that had gone far beyond anything the miners described."

    oren "That would have killed the miners."

    embrum "It almost did."
    embrum "But we are high-level fire-Qana users. Do not mistake resistance for safety."

    story "They walked between the turning flames."
    story "The heat wrapped around them like a brutal wind, yet Oren felt his stomach pool and heart pool answer it, drinking sparks from the air."

    inner_voice "Closer."

    scene bg ruzen titan chamber
    with fade

    show oren neutral at portrait_left
    show embrum neutral at portrait_right
    with dissolve

    story "The tunnel opened into a chamber so large the ceiling vanished into smoke."
    story "At first, Oren thought the far wall was moving."
    story "Then the wall lifted one burning arm."

    show pyroclast_titan neutral at titan_center
    with dissolve

    $ chapter_02_titan_revealed = True
    $ chapter_02_titan_pressure_felt = True

    embrum "No."

    oren "Master Embrum?"

    embrum "Tier three golem."
    embrum "A Titan."

    oren "That is a war engine."

    embrum "Used to break kingdom walls. Used to open cities for invasion."
    embrum "Summoning one is illegal unless the crown demands it for battle."
    embrum "What mage was malicious enough to put this under a village?"

    inner_voice "It has already eaten its fill."

    story "At the Titan's chest, a crystal heart pulsed through plates of black stone."
    story "Every pulse pushed heat into the mountain. Every pulse answered the dry wells above."

    oren "If we fight it loose, it could bring the mountain down."
    oren "The Ruzen mines collapse, the village loses its second export, and we are buried with it."

    embrum "Then we do not fight it loose."
    embrum "One of us keeps its actions small. The other breaks the Qana core."

    oren "The crystal heart."

    embrum "A golem's battery and command center."
    embrum "I will draw its movement. You charge the strike."

    oren "You could be stepped on."

    embrum "That is why I am the one doing it."
    embrum "When the core opens, throw everything you can control. Not everything you feel. Everything you can control."

    story "Embrum moved first."
    story "His fire-Qana flared in clean arcs, not wild, not loud, each strike forcing the Titan to turn without smashing the chamber walls."

    show embrum phoenix_slash at combat_cutin
    with dissolve

    story "The arc became a phoenix of flame, bright enough to pull the Titan's burning gaze away from Oren."

    hide embrum
    with dissolve

    inner_voice "He is brave for a jailer."

    oren "Quiet."

    inner_voice "No. Listen."
    inner_voice "Your fire is a candle. Mine is the thing that taught fire hunger."

    story "White pressure coiled beneath Oren's ribs."
    story "Fire-Qana gathered around his spear until the metal shook."

    embrum "Oren!"

    hide pyroclast_titan
    show pyroclast_titan exposed at titan_cutin
    with dissolve

    story "The Titan raised one foot over Embrum."

    menu:
        "Throw before the core fully opens.":
            $ oren_resolve += 1
            $ qana_strain += 1

            story "Oren threw early, choosing control over perfect power."
            story "The spear struck the edge of the Qana core and cracked it wide enough for the second burst to follow."

        "Trust the voice for one heartbeat longer.":
            $ dragon_pressure += 2
            $ heard_jotunn_claim = True

            inner_voice "Now."
            story "Oren waited one impossible heartbeat."
            story "The core opened like a red eye, and the spear left his hand carrying fire wrapped around white Qana pressure."

        "Anchor yourself on Embrum's warning.":
            $ embrum_trust += 1
            $ oren_resolve += 1

            oren "Everything I can control."
            story "Oren shaped the heat down to a single point and let the white pressure ride inside it like a second spear."

    show oren dragon_spear at combat_cutin
    with dissolve

    story "Dragon Spear tore across the chamber, white Pure Qana braided with Oren's fire-Qana until the air itself split around it."

    hide oren
    with dissolve

    story "The twin spear punched through the Titan's Qana core."
    story "For one breath, the whole mountain glowed from within."

    hide pyroclast_titan
    with dissolve

    scene bg ruzen titan chamber destroyed
    with fade

    show oren neutral at portrait_left
    show embrum neutral at portrait_right
    show pyroclast_titan broken at titan_broken_center
    with dissolve

    story "Then the Titan broke."
    story "Its chest collapsed inward, its limbs lost command, and the fire-Qana pulses that had been beating through Ruzen went silent."

    $ chapter_02_titan_destroyed = True

    embrum "Report language: illegal tier three golem, unknown summoner, likely hostile to crown interests."

    oren "That is all?"

    embrum "That is what we know."
    embrum "The Highguard chief will want answers. So will I."

    inner_voice "They left the weapon. They did not leave the reason."

    story "Above them, Anozira's wells would not refill in a day."
    story "But without the Titan eating lava and pulsing fire-Qana through the mountain, the reservoirs could begin returning on their own."
    story "If the kingdom kept the water shipments coming, the village might survive long enough to forgive the ground."

    scene cg anozira thanks ending
    with fade

    story "Two days later, Anozira's wells still tasted of metal and heat."
    story "But when the buckets came up, they came up wet."
    story "The first water barrels from the kingdom rolled into the village square behind carts of rescued Ruzen crystal and half-salvaged nairn."
    story "Embrum did not stand in front of the thanks."

    embrum "It was all him."

    story "The villagers turned toward Oren with relief too tired to be graceful."
    story "Hands reached for his gauntlet. A child smiled at him like he had dragged the sun back by its throat."

    oren "I only did what Master Embrum told me."

    story "No one heard the warning in that."

    inner_voice "They praise the cage because they have not seen what strains inside it."

    story "Oren lowered his hand before it could tremble."
    story "For one morning, Anozira lived."

    call screen chapter_complete_menu(
        chapter_number="Chapter II",
        chapter_title="Placeholder Trial",
        chapter_location="Anozira Village",
        chapter_summary="The wells are flowing again, but the truth beneath Ruzen is still buried. Oren leaves Anozira with praise on his shoulders and darker questions waiting ahead.",
        chapter_status="Chapter complete",
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
