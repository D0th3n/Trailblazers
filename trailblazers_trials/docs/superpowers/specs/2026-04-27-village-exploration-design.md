# Village Exploration Design

## Goal

Add a first-pass exploration layer to `Trailblazers Trials` inside Ren'Py without turning the project into a separate RPG engine. The exploration beat should feel like a short playable village scene between dialogue blocks, not a replacement for the visual novel structure.

## Scope

This pass adds:

- one small village exploration map
- keyboard tile movement for Oren
- basic collision using blocked tiles
- one optional interaction at a steaming well
- one optional interaction with a villager
- one required interaction with the mayor to return to chapter dialogue
- CC0 placeholder environment art for the map

This pass does not add:

- freeform movement
- combat on the map
- pathfinding or NPC movement
- inventory
- saveable exploration state beyond normal Ren'Py defaults
- isometric depth sorting

## Approach

Use a Ren'Py `screen` as the exploration surface, with `key` bindings for movement and `Return(...)` for event completion. Keep movement logic in a small pure Python helper module so collision and event lookup can be tested outside Ren'Py.

The environment art will be a single composed background built from a public-domain tile pack. The player avatar will be a lightweight placeholder token derived from existing Oren art, which keeps the prototype visually coherent while avoiding a full sprite pipeline before alpha playtesting.

## Chapter Integration

Insert the exploration beat into `chapter_01` after Embrum tells Oren to focus on the crisis and before the mayor briefing scene. The player can inspect the village square briefly, learn one or two contextual details, and then trigger the mayor conversation by walking to him.

## Asset Strategy

Use Kenney's Tiny Town asset pack from the official Kenney site under CC0 for placeholder village map tiles:

- official asset page: `https://kenney.nl/assets/tiny-town`
- official license: `https://creativecommons.org/publicdomain/zero/1.0/`

Only the prototype map image and source archive reference need to be kept in-project for now. Later custom Trailblazers-specific exploration art can replace the composed placeholder background without changing the movement logic.

## Testing Strategy

Test the pure movement model with `pytest`:

- movement inside bounds
- collision rejection on blocked tiles
- event lookup by tile coordinate
- pixel conversion for tile placement

Then verify Ren'Py integration with project lint.
