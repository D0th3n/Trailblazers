# Chapter 1 Polish Design

## Goal

Polish `Chapter 1: Heart of Fire` into a cleaner, more intentional vertical slice before opening `Chapter 2`. This pass should tighten presentation, standardize visuals, improve player-directed investigation, and set up reusable interaction patterns without reopening the whole chapter structure.

## Scope

This pass adds or changes:

- a hard standard that all new scene backgrounds are authored for `16:9`
- a preferred background target of `1920x1080`
- UI/layout changes so exploration and investigation screens are designed around `16:9`
- a larger Anozira village overview with more clickable places
- a mandatory `Tavern` location on the village overview
- story gating so the mine route is locked until the tavern scene is completed
- a revised day/night flow where the village Moglim cleanup takes the day and the mine investigation begins the next morning
- a reusable first-person hotspot scene pattern for “look and choose what to investigate”
- a reusable action-targeting hotspot scene pattern for future body-part / spell / strike selection
- a future-ready “choice battle” format with `2` failure outcomes and `1` success outcome

This pass does not add:

- Chapter 2 content
- full tactical combat
- free movement or sprite walking
- a full failure-state game over system across all of Chapter 1
- replacement art for every legacy background immediately

## Design Principles

1. `Heart of Fire` should stay finishable.
   The goal is to improve Chapter 1 without reopening every scene or multiplying branches uncontrollably.

2. Player agency should feel visual, not only textual.
   Investigation and action should increasingly happen through scene-based hotspot selection rather than only text menus.

3. Shared systems should be reused across contexts.
   The same clickable marker logic should power:
   - village overview navigation
   - tavern investigation scenes
   - future conversation pick-order scenes
   - future action targeting scenes

4. Visual presentation should assume `16:9`.
   UI should be positioned inside a safe center area so modern backgrounds fill the screen cleanly.

## Visual Standardization

### Background Standard

All new backgrounds sent by the user should be treated as:

- target aspect ratio: `16:9`
- preferred working size: `1920x1080`

Older non-`16:9` assets remain temporary placeholders until replaced.

### Layout Rule

Scene composition, hotspot placement, and menu panels should be authored against a `16:9` playfield. UI should avoid living near the extreme edges so slight scaling differences do not create leaks or tearing.

### Temporary Placeholder Policy

If an older background is narrower or taller than `16:9`, it should be:

- centered
- scaled as safely as possible
- treated as temporary until a true `16:9` replacement is provided

No new layout work should be designed around old nonstandard image dimensions.

## Chapter 1 Flow Change

Current flow should be adjusted to:

1. arrival / setup
2. village overview investigation
3. Moglim-related village pressure escalates
4. village spends the day being cleared and stabilized
5. evening tavern scene becomes mandatory
6. tavern investigation / conversations happen at night
7. mine route unlocks the next morning
8. Ruzen mine investigation continues after that

This change supports pacing better than jumping directly from daytime village beats to the mines.

## Village Overview Expansion

The static Anozira overview remains a click-on-marker scene, but it becomes richer.

### Required Clickable Locations

At minimum, the village overview should support:

- `Well`
- `Villager`
- `Tavern`
- `Embrum` or market continuation marker

Additional placeholder-capable locations can be added later, but these are the required first set.

### Tavern Rule

`Tavern` must be mandatory.

The mine route should remain locked until:

- the player visits the tavern
- the tavern scene finishes
- the next-morning transition occurs

### Marker Behavior

Village markers should use the same visible clickable label style:

- strong readable label box
- short category text like `TALK`, `WELL`, `TAVERN`
- second line for the specific place/person name

## First-Person Investigation Scenes

The next interaction layer should move beyond birds-eye maps.

### Concept

A first-person or over-the-shoulder scene displays a composed background. The player chooses who or what to investigate by clicking on labeled hotspots placed directly over the scene.

### Tavern Example

In the tavern, Oren may see a room full of possible conversation targets. The player should click who to approach first rather than choosing from a plain text menu.

Example tavern targets:

- drunk villager
- worker at the bar
- water carrier
- miner / foreman

The actual cast can be finalized later, but the system should support a clear first click that opens the next dialogue segment.

### Why This Matters

This keeps the VN readable while making the player feel like they are selecting from the scene itself, not only from abstract option text.

## Action Targeting Scenes

The same hotspot engine should later support action decisions.

### Concept

Instead of choosing from a plain menu, the player sees a composed combat or danger scene with labeled markers on:

- enemy body areas
- environmental hazards
- friendly targets
- spell aim points

### Early Chapter 1 Use

The first target use can be a small choice-battle sequence such as:

- a villager asks Oren to stop a speeding Moglim before it hits a cart of water barrels
- the player clicks one of several target areas or response points

### Future Boss Use

The Titan scene can later reuse this pattern by placing markers on:

- core
- limbs
- footing
- environmental supports

## Choice Battle Format

New micro-battle dialogue scenes should follow a simple three-outcome structure:

- `1` correct outcome
- `2` failure outcomes

### Failure Meaning

Failure does not have to mean immediate game over.

It can mean:

- civilian harm
- lost trust
- a harsher follow-up line from Embrum
- wasted time
- a rougher transition into the next scene

### Success Meaning

Success should reward:

- cleaner scene resolution
- stronger Oren competence
- better emotional impression
- optional trust or chapter-state benefits later

## Reusable System Strategy

This polish pass should not build separate systems for every scene type.

Instead, it should produce one shared hotspot-driven interaction framework that can be configured differently for:

- overview maps
- room investigation scenes
- conversation target selection
- action target selection

### Shared Inputs

Each scene should be configurable through:

- a background image
- a scene title / objective line
- a list of hotspots
- hotspot labels
- hotspot coordinates
- hotspot result target
- optional lock/unlock conditions

## Story Gating

Chapter 1 progression should use explicit flags.

Minimum gating concepts:

- village scene visited
- tavern unlocked
- tavern completed
- mine unlocked

The mine should not appear as the next logical step until tavern completion is true.

## Asset Expectations

For best results, the user should provide future images in `1920x1080`.

### Immediate Asset Needs After This Pass

Once implementation begins, the most useful new assets will be:

- `16:9` tavern interior background
- `16:9` next-morning mine route background
- `16:9` first-person tavern perspective scene
- any new `16:9` village sublocation backgrounds the user wants clickable

## Testing Strategy

Tests should verify:

- scene config validity for the expanded hotspot system
- required marker presence on the village overview
- mine gating remains locked before tavern completion
- mine unlocks after tavern completion
- hotspot definitions resolve to valid scene targets

Ren'Py verification should also confirm:

- village overview renders at `16:9` safely
- choice/investigation panels stay readable over bright backgrounds
- tavern marker opens the correct continuation path

## Implementation Order

Once the user approves this design, the recommended build order is:

1. adapt scene and hotspot layout assumptions to `16:9`
2. expand the village overview and add the mandatory `Tavern` marker
3. add story gating so the mine unlocks only after tavern completion
4. build the first-person tavern investigation shell
5. add the first Chapter 1 choice-battle scene
6. polish transitions into the next-morning mine route
