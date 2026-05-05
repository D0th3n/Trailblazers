# Asset Manifest

Source folders:

- `/Users/murks/Documents/Documents - murks’s MacBook Pro/Codex/2026-04-18-trailblazers-trials-i-want-to-create/Player-sprites`
- `/Users/murks/Documents/Documents - murks’s MacBook Pro/Codex/2026-04-18-trailblazers-trials-i-want-to-create/NPC-sprites`

Curated Ren'Py copies:

- `images/backgrounds/village_dawn_drought.png`
- `images/backgrounds/village_road_day.png`
- `images/backgrounds/village_square_day.png`
- `images/backgrounds/village_square_dusk.png`
- `images/backgrounds/nairn_fields_dusk.png`
- `images/backgrounds/nairn_fields_day.png`
- `images/backgrounds/ruzen_mine_entrance.png`
- `images/backgrounds/ruzen_upper_tunnel.png`
- `images/backgrounds/ruzen_deep_passage.png`
- `images/backgrounds/ruzen_fire_tornado_passage.png`
- `images/backgrounds/ruzen_titan_chamber.png`
- `images/backgrounds/ruzen_titan_chamber_destroyed.png`
- `images/backgrounds/tavern_night.png`
- `images/backgrounds/cleric_office.png`
- `images/backgrounds/village_square_night.png`
- `images/exploration/anozira_square_map.png`
- `images/exploration/oren_map_token.png`
- `images/characters/oren_squire.png`
- `images/references/combat/oren_action_spear.png`
- `images/references/combat/oren_dragon_spear_spell.png`
- `images/references/combat/embrum_phoenix_flame_slash.png`
- `images/cg/anozira_thanks_ending.png`
- `images/references/characters/oren_squire_old.png`
- `images/references/characters/oren_squire_white_canvas.png`
- `images/references/characters/oren_squire_source_20260423_0010.png`
- `images/references/characters/oren_squire_previous_active_20260422.png`
- `images/references/characters/oren_squire_previous_active_20260423_0010.png`
- `images/characters/embrum_mentor.png`
- `images/references/characters/embrum_mentor_source_20260422_232443.png`
- `images/references/characters/embrum_mentor_previous_active_20260422.png`
- `images/references/characters/embrum_mentor_previous_active_20260422_232443.png`
- `images/characters/village_guard.png`
- `images/references/characters/village_guard_source_20260422_122042.png`
- `images/references/characters/village_guard_previous_active_20260422.png`
- `images/characters/villager.png`
- `images/references/characters/villager_pixel_old.png`
- `images/characters/village_mayor.png`
- `images/references/characters/village_mayor_white_canvas.png`
- `images/characters/eldran_merchant.png`
- `images/references/characters/eldran_merchant_white_canvas.png`
- `images/characters/highguard_knight_portrait.png`
- `images/references/characters/highguard_knight_portrait_white_canvas.png`
- `images/characters/water_worker.png`
- `images/characters/medic_cleric.png`
- `images/characters/drunk_father.png`
- `images/characters/village_woman.png`
- `images/characters/village_daughter.png`
- `images/characters/wounded_miner.png`
- `images/characters/miner.png`
- `images/characters/miner_foreman.png`
- `images/enemies/drought_creature.png`
- `images/enemies/drought_creature.png` is currently mapped in code as `moglim neutral`.
- `images/enemies/moglim_mogul.png`
- `images/enemies/pyroclast_titan_golem.png`
- `images/enemies/pyroclast_titan_core_exposed.png`
- `images/enemies/pyroclast_titan_broken.png`
- `images/enemies/slime.png` remains as an unused legacy placeholder.
- `skeleton neutral`, `beast neutral`, and `golem boss` are now safe color placeholders in `images.rpy` until real enemy art is added.
- `images/props/empty_nairn_cart.png`
- `images/props/water_cart_worker.png`
- `images/props/defeated_moglim.png`
- `images/references/imports/` contains source copies and replaced active copies from the April 22 Ruzen/miner/prop import pass.
- `images/references/imports/` also contains source copies from the April 22 evening village interlude import pass.
- `images/references/imports/` also contains source copies from the April 22 deep Ruzen boss-fight background import pass.
- `images/references/imports/` also contains source copies from the April 22 Titan boss phase import pass.
- `images/references/imports/` also contains source copies from the April 22 Oren/Embrum combat cut-in import pass.
- `images/references/imports/` also contains the April 22 cave Mogul source file.
- `images/references/public_assets/kenney_tiny-town.zip` and `images/references/public_assets/kenney_tiny_town/` preserve the Kenney Tiny Town CC0 source used for the chapter 1 exploration prototype.

Notes:

- The current prototype uses raw sprite art with simple zoom transforms.
- Sprite normalization should happen in the next pass.
- The current chapter now includes a tavern, medic-cleric office, and night-square interlude before the Ruzen mine approach.
- The current chapter now uses dedicated deep Ruzen passage, fire-tornado passage, Titan chamber, and destroyed-chamber backgrounds for the boss route.
- The current chapter now uses three Titan phase images: discovery, exposed core cut-in, and defeated body.
- The current chapter now uses Oren's Dragon Spear and Embrum's Phoenix Flame Slash as full-screen combat cut-ins.
- The current chapter now includes a short pre-story intro and an Anozira thank-you ending CG.
- The cave Moglim group encounter now uses the dedicated `moglim_mogul.png` image.
- The current chapter now includes a small keyboard exploration layer in Anozira Square using `images/exploration/anozira_square_map.png` and `images/exploration/oren_map_token.png`.
- `oren_squire.png` is the mandatory Oren dialogue sprite for all dialogue scenes.
- `embrum_mentor.png` is the mandatory Master Embrum dialogue sprite for all dialogue scenes.
- Several source images appear to be alternate poses or compositions; only one per role was copied for the first pass.
- Multi-view sheets and action illustrations are stored under `images/references/` for future cropping and sprite work.
