image bg village dawn = "images/backgrounds/village_dawn_drought.png"
image bg village road day = "images/backgrounds/village_road_day.png"
image bg village square = "images/backgrounds/village_square_day.png"
image bg village square dusk = "images/backgrounds/village_square_dusk.png"
image bg nairn fields = "images/backgrounds/nairn_fields_dusk.png"
image bg nairn fields day = "images/backgrounds/nairn_fields_day.png"
image bg forest edge = "images/backgrounds/nairn_fields_dusk.png"
image bg ruzen mine entrance = "images/backgrounds/ruzen_mine_entrance.png"
image bg ruzen upper tunnel = "images/backgrounds/ruzen_upper_tunnel.png"
image bg ruzen deep passage = "images/backgrounds/ruzen_deep_passage.png"
image bg ruzen fire tornado passage = "images/backgrounds/ruzen_fire_tornado_passage.png"
image bg ruzen titan chamber = "images/backgrounds/ruzen_titan_chamber.png"
image bg ruzen titan chamber destroyed = "images/backgrounds/ruzen_titan_chamber_destroyed.png"
image bg tavern night = "images/backgrounds/tavern_night.png"
image bg cleric office = "images/backgrounds/cleric_office.png"
image bg village square night = "images/backgrounds/village_square_night.png"
image bg anozira exploration = Transform("images/exploration/anozira_village_backdrop.png", xysize=(1600, 900))
image menu title background = "images/menu/title_background.png"
image menu title logo = "images/menu/trailblazers_logo.png"
image bg memory white = Solid("#f7f4e8")
image bg severance dark = Solid("#161421")

image cg anozira thanks ending = "images/cg/anozira_thanks_ending.png"
image cg chapter_02_oren_waking = "images/cg/chapter_02/oren_waking.png"
image cg chapter_02_oren_armoring = "images/cg/chapter_02/oren_armoring.png"
image cg chapter_02_oren_hallway = "images/cg/chapter_02/oren_hallway.png"

image oren neutral = "images/characters/oren_squire.png"
image side oren neutral = "images/characters/side/oren_neutral.png"
image side oren focused = "images/characters/side/oren_focused.png"
image side oren annoyed = "images/characters/side/oren_annoyed.png"
image side oren uneasy = "images/characters/side/oren_uneasy.png"
image side oren confident = "images/characters/side/oren_confident.png"
image oren action = "images/references/combat/oren_action_spear.png"
image oren dragon_spear = "images/references/combat/oren_dragon_spear_spell.png"
image embrum phoenix_slash = "images/references/combat/embrum_phoenix_flame_slash.png"
image combat oren temp idle = "images/combat/oren_temp_idle.png"
image combat training dummy temp idle = "images/combat/training_dummy_temp_idle.png"
image embrum neutral = "images/characters/embrum_mentor.png"
image guard neutral = "images/characters/village_guard.png"
image villager neutral = "images/characters/villager.png"
image mayor neutral = "images/characters/village_mayor.png"
image eldran merchant neutral = "images/characters/eldran_merchant.png"
image highguard neutral = "images/characters/highguard_knight_portrait.png"
image water_worker neutral = "images/characters/water_worker.png"
image miner neutral = "images/characters/miner.png"
image miner_foreman neutral = "images/characters/miner_foreman.png"
image medic_cleric neutral = "images/characters/medic_cleric.png"
image drunk_father neutral = "images/characters/drunk_father.png"
image village_woman neutral = "images/characters/village_woman.png"
image village_daughter neutral = "images/characters/village_daughter.png"
image wounded_miner neutral = "images/characters/wounded_miner.png"

image drought_creature neutral = "images/enemies/drought_creature.png"
image moglim neutral = "images/enemies/drought_creature.png"
image moglim mogul = "images/enemies/moglim_mogul.png"
image skeleton neutral = Solid("#5b554e")
image beast neutral = Solid("#4d3f35")
image golem boss = Solid("#362f2b")
image pyroclast_titan neutral = "images/enemies/pyroclast_titan_golem.png"
image pyroclast_titan exposed = "images/enemies/pyroclast_titan_core_exposed.png"
image pyroclast_titan broken = "images/enemies/pyroclast_titan_broken.png"

image prop empty_nairn_cart = "images/props/empty_nairn_cart.png"
image prop water_cart_worker = "images/props/water_cart_worker.png"
image prop defeated_moglim = "images/props/defeated_moglim.png"
image oren map token = Transform(
    Crop((20, 0, 128, 192), "images/exploration/oren_map_chibi_sheet.png"),
    zoom=0.34,
    nearest=True,
)

transform portrait_left:
    xalign 0.08
    yalign 1.0
    zoom 0.27

transform portrait_right:
    xalign 0.92
    yalign 1.0
    zoom 0.27

transform portrait_center:
    xalign 0.5
    yalign 1.0
    zoom 0.27

transform enemy_center:
    xalign 0.5
    yalign 0.92
    zoom 0.42

transform mogul_center:
    xalign 0.5
    yalign 0.94
    zoom 0.62

transform titan_center:
    xalign 0.5
    yalign 1.0
    zoom 0.55

transform titan_cutin:
    xalign 0.5
    yalign 0.5
    zoom 0.64

transform titan_broken_center:
    xalign 0.5
    yalign 1.0
    zoom 0.58

transform prop_right:
    xalign 0.84
    yalign 1.0
    zoom 0.34

transform prop_evidence:
    xalign 0.52
    yalign 0.98
    zoom 0.18

transform memory_flash:
    alpha 0.0
    linear 0.25 alpha 1.0
    linear 0.45 alpha 0.0

transform combat_cutin:
    xalign 0.5
    yalign 0.5
    zoom 1.0
