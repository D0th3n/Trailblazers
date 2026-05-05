# Village Exploration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a small keyboard-driven village exploration layer to chapter 1 and return to visual-novel dialogue when the player reaches the mayor.

**Architecture:** Keep Ren'Py UI logic in a new exploration system file and keep movement/collision math in a separate pure Python helper module. Compose a single placeholder map image from CC0 tiles so the prototype is easy to replace later without rewriting the screen logic.

**Tech Stack:** Ren'Py screen language, Python helper module, pytest, Pillow, Kenney Tiny Town CC0 tiles.

---

### Task 1: Build and test the pure movement model

**Files:**
- Create: `trailblazers_trials_renpy/game/exploration_model.py`
- Create: `trailblazers_trials_renpy/tests/test_exploration_model.py`

- [ ] Write failing tests for movement, collision, event lookup, and tile-to-pixel conversion.
- [ ] Run the tests and confirm they fail for the missing module/functions.
- [ ] Add the smallest pure Python implementation needed to pass those tests.
- [ ] Re-run the tests and confirm they pass.

### Task 2: Import placeholder public assets and compose the map

**Files:**
- Create: `trailblazers_trials_renpy/game/images/exploration/anozira_square_map.png`
- Create: `trailblazers_trials_renpy/game/images/exploration/oren_map_token.png`
- Modify: `trailblazers_trials_renpy/docs/ASSET_IMPORT_MAP.md`
- Modify: `trailblazers_trials_renpy/game/data/asset_manifest.md`

- [ ] Extract the Kenney Tiny Town pack into references for provenance.
- [ ] Compose one 20x11 tile village map image for the prototype.
- [ ] Generate a placeholder Oren exploration token from existing local art.
- [ ] Document the imported public assets and prototype-specific outputs.

### Task 3: Add the Ren'Py exploration system

**Files:**
- Create: `trailblazers_trials_renpy/game/systems/exploration.rpy`
- Modify: `trailblazers_trials_renpy/game/images.rpy`
- Modify: `trailblazers_trials_renpy/game/variables.rpy`

- [ ] Define map metadata, blocked tiles, optional event tiles, and HUD copy.
- [ ] Add a modal exploration screen with keyboard movement and interaction prompts.
- [ ] Return a string result when the player activates an event tile.
- [ ] Add image declarations/transforms for the new map and token.
- [ ] Add any minimal state defaults needed for the chapter flow.

### Task 4: Integrate chapter 1

**Files:**
- Modify: `trailblazers_trials_renpy/game/chapters/chapter_01.rpy`

- [ ] Replace the immediate jump to the mayor scene with a short exploration label call.
- [ ] Add one optional steaming-well interaction and one optional villager interaction.
- [ ] Resume the existing mayor dialogue when the required mayor event is reached.

### Task 5: Verify

**Files:**
- No new files

- [ ] Run `pytest` for the exploration model tests.
- [ ] Run Ren'Py lint with `/Users/murks/Web-Projects/renpy-8.5.2-sdk/renpy.sh trailblazers_trials_renpy lint`.
- [ ] Fix any issues surfaced by either verification step before claiming completion.
