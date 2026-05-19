# Chapter 1 Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Standardize Chapter 1 around 16:9 presentation, expand the Anozira hotspot flow with a mandatory tavern night scene, and introduce reusable first-person hotspot and choice-battle systems before Chapter 2 begins.

**Architecture:** Keep scene configuration and validation in pure Python so the hotspot layouts, story gates, and outcome wiring can be tested outside Ren'Py. Keep all rendering and interaction in Ren'Py screens, but drive those screens from a single hotspot scene registry that can power overview maps, tavern investigation scenes, and action-targeting scenes.

**Tech Stack:** Ren'Py screen language, Python helper modules, Python `unittest`, existing Chapter 1 labels, existing character/background assets, 1600x900 in-engine canvas authored for 16:9 source art.

---

## File Structure

### New or expanded responsibilities

- `trailblazers_trials/game/hotspot_scene_data.py`
  - Pure Python registry for hotspot scenes.
  - Stores scene IDs, background names, objective text, hotspot labels, hotspot coordinates, target labels, and gate conditions.
  - Keeps the Anozira overview, tavern first-person scene, and action-targeting scenes in one shape.

- `trailblazers_trials/game/hotspot_scene_model.py`
  - Pure Python helpers for hotspot validation and progression rules.
  - Validates 16:9-safe coordinates and hotspot scene completeness.
  - Computes available hotspots based on current story flags.

- `trailblazers_trials/game/systems/exploration.rpy`
  - Ren'Py renderer for hotspot scenes.
  - Replaces the current village-only exploration assumptions with a generic scene-based hotspot UI.

- `trailblazers_trials/game/exploration_data.py`
  - Legacy compatibility module for older exploration tests and imports.
  - Should stay lightweight and untouched unless a runtime import still depends on it.

- `trailblazers_trials/game/chapters/chapter_01.rpy`
  - Story flow updates:
    - daytime village investigation
    - mandatory tavern night
    - next-morning mine unlock
    - first choice-battle insertion

- `trailblazers_trials/game/systems/simple_battle.rpy`
  - Reworked to host the first hotspot-based choice battle instead of a plain text menu.

- `trailblazers_trials/game/images.rpy`
  - Standardize the exploration background declarations around 16:9 scaling and new hotspot backdrops.

- `trailblazers_trials/game/variables.rpy`
  - Add gating flags for tavern access, tavern completion, and mine unlock state.

- `trailblazers_trials/tests/test_hotspot_scene_model.py`
  - Pure Python tests for scene config validity, visible hotspot filtering, and 16:9-safe hotspot placement.

- `trailblazers_trials/tests/test_chapter_01_flow.py`
  - Pure Python tests for Chapter 1 gating and checkpoint expectations.

### Existing files to keep in mind

- `trailblazers_trials/game/screens.rpy`
  - Already contains top-of-screen readability panels and custom menu screens.
  - Should only be modified if the generic hotspot scene renderer needs a shared style or reusable screen wrapper.

- `trailblazers_trials/game/images/backgrounds/tavern_night.png`
  - Existing placeholder tavern backdrop until the user provides a final 16:9 replacement.

- `trailblazers_trials/game/images/exploration/anozira_village_backdrop.png`
  - Existing Anozira overview art that will remain the live overview backdrop until replaced by a newer 16:9 version.

---

### Task 1: Build the shared hotspot scene data/model layer

**Files:**
- Create: `trailblazers_trials/game/hotspot_scene_data.py`
- Create: `trailblazers_trials/game/hotspot_scene_model.py`
- Create: `trailblazers_trials/tests/test_hotspot_scene_model.py`

- [ ] **Step 1: Write the failing tests for shared hotspot scene validation**

```python
from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "game"
if str(GAME_DIR) not in sys.path:
    sys.path.insert(0, str(GAME_DIR))


from hotspot_scene_data import HOTSPOT_SCENES
from hotspot_scene_model import (
    available_hotspots,
    validate_hotspot_scene,
    validate_hotspot_registry,
)


class HotspotSceneModelTests(unittest.TestCase):

    def test_all_hotspot_scenes_are_valid(self):
        self.assertEqual(validate_hotspot_registry(HOTSPOT_SCENES), [])

    def test_anozira_overview_contains_tavern_and_mine_hotspots(self):
        scene = HOTSPOT_SCENES["anozira_overview"]

        hotspot_ids = [hotspot["id"] for hotspot in scene["hotspots"]]

        self.assertIn("well", hotspot_ids)
        self.assertIn("villager", hotspot_ids)
        self.assertIn("market_day", hotspot_ids)
        self.assertIn("tavern", hotspot_ids)
        self.assertIn("mine_path", hotspot_ids)

    def test_market_is_visible_before_evening_unlocks(self):
        scene = HOTSPOT_SCENES["anozira_overview"]
        visible = available_hotspots(
            scene,
            {
                "tavern_unlocked": False,
                "mine_unlocked": False,
            },
        )

        hotspot_ids = [hotspot["id"] for hotspot in visible]

        self.assertIn("market_day", hotspot_ids)
        self.assertNotIn("tavern", hotspot_ids)
        self.assertNotIn("mine_path", hotspot_ids)

    def test_tavern_and_mine_unlock_in_order(self):
        scene = HOTSPOT_SCENES["anozira_overview"]

        evening = available_hotspots(
            scene,
            {
                "tavern_unlocked": True,
                "mine_unlocked": False,
            },
        )
        dawn = available_hotspots(
            scene,
            {
                "tavern_unlocked": True,
                "mine_unlocked": True,
            },
        )

        self.assertIn("tavern", [hotspot["id"] for hotspot in evening])
        self.assertNotIn("mine_path", [hotspot["id"] for hotspot in evening])
        self.assertIn("mine_path", [hotspot["id"] for hotspot in dawn])

    def test_hotspots_stay_inside_16_by_9_safe_area(self):
        for scene in HOTSPOT_SCENES.values():
            problems = validate_hotspot_scene(scene)
            self.assertNotIn("hotspot_out_of_bounds", " ".join(problems))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify the new modules do not exist yet**

Run:

```bash
python3 -m unittest trailblazers_trials.tests.test_hotspot_scene_model -v
```

Expected:

```text
ERROR: Failed to import test module: test_hotspot_scene_model
ModuleNotFoundError: No module named 'hotspot_scene_data'
```

- [ ] **Step 3: Write the minimal hotspot scene registry and validation helpers**

Create `trailblazers_trials/game/hotspot_scene_data.py`:

```python
SCREEN_W = 1600
SCREEN_H = 900


HOTSPOT_SCENES = {
    "anozira_overview": {
        "id": "anozira_overview",
        "background": "bg anozira exploration",
        "title": "Anozira Village Investigation",
        "objective": "Choose where Oren investigates during the day. The tavern is mandatory before the mine opens at dawn.",
        "hotspots": [
            {
                "id": "well",
                "marker": "WELL",
                "short_label": "Well",
                "title": "Inspect the steaming well",
                "x": 805,
                "y": 360,
                "target": "well",
            },
            {
                "id": "villager",
                "marker": "TALK",
                "short_label": "Villager",
                "title": "Talk to the frightened villager",
                "x": 1120,
                "y": 600,
                "target": "villager",
            },
            {
                "id": "market_day",
                "marker": "TALK",
                "short_label": "Embrum",
                "title": "Meet Embrum at the village market",
                "x": 315,
                "y": 675,
                "target": "market_day",
            },
            {
                "id": "tavern",
                "marker": "TAVERN",
                "short_label": "Tavern",
                "title": "Spend the evening in the tavern",
                "x": 420,
                "y": 655,
                "target": "tavern",
                "requires": ["tavern_unlocked"],
            },
            {
                "id": "mine_path",
                "marker": "GO",
                "short_label": "Ruzen Path",
                "title": "Follow Embrum toward the Ruzen mines at first light",
                "x": 1320,
                "y": 250,
                "target": "mine_path",
                "requires": ["mine_unlocked"],
            },
        ],
    },
    "tavern_room": {
        "id": "tavern_room",
        "background": "bg tavern night",
        "title": "Anozira Tavern",
        "objective": "Choose who Oren speaks to first before the mine briefing ends for the night.",
        "hotspots": [
            {
                "id": "drunk_father",
                "marker": "TALK",
                "short_label": "Drunk Father",
                "title": "Speak to Brann's father",
                "x": 355,
                "y": 505,
                "target": "drunk_father",
            },
            {
                "id": "wounded_miner",
                "marker": "TALK",
                "short_label": "Wounded Miner",
                "title": "Speak to the wounded miner",
                "x": 900,
                "y": 460,
                "target": "wounded_miner",
            },
            {
                "id": "leave_tavern",
                "marker": "GO",
                "short_label": "Embrum",
                "title": "Finish the tavern scene and return to Embrum",
                "x": 1270,
                "y": 210,
                "target": "leave_tavern",
                "requires": ["heard_dead_miner_hint"],
            },
        ],
    },
}
```

Create `trailblazers_trials/game/hotspot_scene_model.py`:

```python
from hotspot_scene_data import SCREEN_H, SCREEN_W


def validate_hotspot_scene(scene):
    problems = []

    if "background" not in scene:
        problems.append("missing_background")
    if "hotspots" not in scene or not scene["hotspots"]:
        problems.append("missing_hotspots")

    for hotspot in scene.get("hotspots", []):
        if hotspot["x"] < 0 or hotspot["x"] > SCREEN_W:
            problems.append("hotspot_out_of_bounds:%s" % hotspot["id"])
        if hotspot["y"] < 0 or hotspot["y"] > SCREEN_H:
            problems.append("hotspot_out_of_bounds:%s" % hotspot["id"])

    return problems


def validate_hotspot_registry(registry):
    problems = []

    for scene_id, scene in registry.items():
        for problem in validate_hotspot_scene(scene):
            problems.append("%s:%s" % (scene_id, problem))

    return problems


def available_hotspots(scene, flags):
    visible = []
    for hotspot in scene["hotspots"]:
        required = hotspot.get("requires", [])
        if all(flags.get(flag, False) for flag in required):
            visible.append(hotspot)
        elif not required:
            visible.append(hotspot)
    return visible
```

- [ ] **Step 4: Run the hotspot scene tests and verify they pass**

Run:

```bash
python3 -m unittest trailblazers_trials.tests.test_hotspot_scene_model -v
```

Expected:

```text
OK
```

- [ ] **Step 5: Commit the shared hotspot model**

```bash
git add \
  trailblazers_trials/game/hotspot_scene_data.py \
  trailblazers_trials/game/hotspot_scene_model.py \
  trailblazers_trials/tests/test_hotspot_scene_model.py
git commit -m "feat: add shared hotspot scene model"
```

### Task 2: Convert the Anozira overview to the shared 16:9 hotspot system

**Files:**
- Modify: `trailblazers_trials/game/systems/exploration.rpy`
- Modify: `trailblazers_trials/game/images.rpy`
- Modify: `trailblazers_trials/game/variables.rpy`
- Test: `trailblazers_trials/tests/test_hotspot_scene_model.py`
- Create: `trailblazers_trials/tests/test_chapter_01_flow.py`

- [ ] **Step 1: Write failing tests for story gating flags and tavern-before-mine behavior**

```python
from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "game"
if str(GAME_DIR) not in sys.path:
    sys.path.insert(0, str(GAME_DIR))


from hotspot_scene_data import HOTSPOT_SCENES
from hotspot_scene_model import available_hotspots


class Chapter01FlowTests(unittest.TestCase):

    def test_anozira_overview_hides_tavern_until_evening(self):
        scene = HOTSPOT_SCENES["anozira_overview"]
        visible = available_hotspots(scene, {"tavern_unlocked": False, "mine_unlocked": False})

        hotspot_ids = [hotspot["id"] for hotspot in visible]

        self.assertIn("market_day", hotspot_ids)
        self.assertNotIn("tavern", hotspot_ids)
        self.assertNotIn("mine_path", hotspot_ids)

    def test_anozira_overview_shows_tavern_after_evening_unlock(self):
        scene = HOTSPOT_SCENES["anozira_overview"]
        visible = available_hotspots(scene, {"tavern_unlocked": True, "mine_unlocked": False})

        hotspot_ids = [hotspot["id"] for hotspot in visible]

        self.assertIn("tavern", hotspot_ids)
        self.assertNotIn("mine_path", hotspot_ids)

    def test_anozira_overview_shows_mine_after_tavern_completion(self):
        scene = HOTSPOT_SCENES["anozira_overview"]
        visible = available_hotspots(scene, {"tavern_unlocked": True, "mine_unlocked": True})

        hotspot_ids = [hotspot["id"] for hotspot in visible]

        self.assertIn("mine_path", hotspot_ids)
```

- [ ] **Step 2: Run the new Chapter 1 flow tests and verify the file/module is still missing**

Run:

```bash
python3 -m unittest trailblazers_trials.tests.test_chapter_01_flow -v
```

Expected:

```text
ERROR: Failed to import test module: test_chapter_01_flow
ModuleNotFoundError: No module named 'trailblazers_trials.tests.test_chapter_01_flow'
```

- [ ] **Step 3: Add the Chapter 1 gating defaults and retarget the exploration screen to the new scene registry**

Modify `trailblazers_trials/game/variables.rpy`:

```renpy
default visited_tavern = False
default tavern_unlocked = False
default tavern_completed = False
default mine_unlocked = False
default visited_village_overview = False
default explored_village_well = False
default explored_village_rumor = False
```

Modify the top of `trailblazers_trials/game/images.rpy` so overview backgrounds consistently scale to the live 16:9 canvas:

```renpy
image bg anozira exploration = Transform(
    "images/exploration/anozira_village_backdrop.png",
    xysize=(1600, 900),
)
image bg tavern first person = Transform(
    "images/backgrounds/tavern_night.png",
    xysize=(1600, 900),
)
```

Modify `trailblazers_trials/game/systems/exploration.rpy` so it imports the shared scene registry, replaces the old map-only helpers, and renders generic hotspots:

```renpy
init python:
    import hotspot_scene_data
    import hotspot_scene_model

    HOTSPOT_SCENES = hotspot_scene_data.HOTSPOT_SCENES

    def hotspot_scene(scene_id):
        return HOTSPOT_SCENES[scene_id]

    def hotspot_scene_current():
        return hotspot_scene(store.exploration_map_id)

    def hotspot_scene_flags():
        return {
            "visited_tavern": bool(store.visited_tavern),
            "tavern_unlocked": bool(store.tavern_unlocked),
            "tavern_completed": bool(store.tavern_completed),
            "mine_unlocked": bool(store.mine_unlocked),
            "heard_dead_miner_hint": bool(store.heard_dead_miner_hint),
        }

    def hotspot_scene_visible_hotspots(scene_id):
        return hotspot_scene_model.available_hotspots(
            hotspot_scene(scene_id),
            hotspot_scene_flags(),
        )

    def hotspot_scene_progress_text(scene_id):
        visible = hotspot_scene_visible_hotspots(scene_id)
        labels = [hotspot["short_label"] for hotspot in visible]
        return "Available: %s." % ", ".join(labels)
```

Replace the body of `screen exploration_screen():` so it reads from the hotspot scene shape instead of `map_data`:

```renpy
screen exploration_screen():
    modal True
    zorder 100

    $ scene = hotspot_scene_current()

    add scene["background"]

    for hotspot in hotspot_scene_visible_hotspots(store.exploration_map_id):
        button:
            xpos hotspot["x"]
            ypos hotspot["y"]
            xanchor 0.5
            yanchor 0.5
            xpadding 18
            ypadding 10
            background Solid("#1d0d08ee")
            hover_background Solid("#5c3218ee")
            action Return(hotspot["target"])

            vbox:
                spacing 1
                xalign 0.5
                text hotspot["marker"] color "#f7dd9b" size 26 xalign 0.5
                text hotspot["short_label"] color "#fff6df" size 18 xalign 0.5

    frame:
        background Solid("#140d09d8")
        xalign 0.5
        yalign 0.03
        xmaximum 1120
        xpadding 20
        ypadding 12

        vbox:
            spacing 4
            text scene["title"] color "#f7dd9b" size 24
            text scene["objective"] color "#f3ebe3" size 16

    frame:
        background Solid("#140d09d8")
        xalign 0.5
        yalign 0.94
        xmaximum 1160
        xpadding 20
        ypadding 12

        vbox:
            spacing 4
            text hotspot_scene_progress_text(store.exploration_map_id) color "#f0d8b8" size 14
            text "Mouse only: click a marker to investigate or continue." color "#d8c8bf" size 13
```

- [ ] **Step 4: Add the Chapter 1 flow tests and run them**

Create `trailblazers_trials/tests/test_chapter_01_flow.py` with the code from Step 1, then run:

```bash
python3 -m unittest trailblazers_trials.tests.test_chapter_01_flow -v
```

Expected:

```text
OK
```

- [ ] **Step 5: Commit the 16:9 overview conversion and gating**

```bash
git add \
  trailblazers_trials/game/systems/exploration.rpy \
  trailblazers_trials/game/images.rpy \
  trailblazers_trials/game/variables.rpy \
  trailblazers_trials/tests/test_chapter_01_flow.py
git commit -m "feat: convert Anozira overview to gated hotspot scene"
```

### Task 3: Rewire Chapter 1 day/night progression and make Tavern mandatory

**Files:**
- Modify: `trailblazers_trials/game/chapters/chapter_01.rpy`
- Test: `trailblazers_trials/tests/test_chapter_01_flow.py`

- [ ] **Step 1: Extend the Chapter 1 flow tests to describe the new mine lock expectations**

Append to `trailblazers_trials/tests/test_chapter_01_flow.py`:

```python
    def test_tavern_scene_exposes_leave_hotspot_only_after_hint(self):
        scene = HOTSPOT_SCENES["tavern_room"]

        before = available_hotspots(scene, {"heard_dead_miner_hint": False})
        after = available_hotspots(scene, {"heard_dead_miner_hint": True})

        self.assertNotIn("leave_tavern", [hotspot["id"] for hotspot in before])
        self.assertIn("leave_tavern", [hotspot["id"] for hotspot in after])
```

- [ ] **Step 2: Run the Chapter 1 flow tests to confirm the tavern leave gate is not wired yet**

Run:

```bash
python3 -m unittest trailblazers_trials.tests.test_chapter_01_flow -v
```

Expected:

```text
FAIL: test_tavern_scene_exposes_leave_hotspot_only_after_hint
AssertionError: 'leave_tavern' unexpectedly found in ['drunk_father', 'wounded_miner', 'leave_tavern']
```

- [ ] **Step 3: Rewrite the overview exit and tavern night labels in Chapter 1**

Modify `trailblazers_trials/game/chapters/chapter_01.rpy` so the overview returns to specific next steps:

```renpy
label anozira_square_exploration:

    $ visited_village_overview = True
    $ exploration_begin("anozira_overview", reset_position=True)

    while True:
        call screen exploration_screen

        if _return == "well":
            $ explored_village_well = True
            call anozira_overview_well
        elif _return == "villager":
            $ explored_village_rumor = True
            call anozira_overview_villager
        elif _return == "market_day":
            return
        elif _return == "tavern":
            jump anozira_evening_interlude
        elif _return == "mine_path":
            jump ruzen_mine_approach
```

After the market briefing and the Chapter 1 Moglim cleanup scene, set the evening unlock and re-open the village overview:

```renpy
    $ tavern_unlocked = True
    story "The Moglim cleanup took the village until sunset. By the time the last hot stones stopped rolling, Embrum turned away from the mine road."
    story "Ruzen could wait until morning. Tonight, the tavern would tell them what fear said after drink loosened it."
    call anozira_square_exploration
```

Create small return labels for the daytime overview:

```renpy
label anozira_overview_well:
    scene bg village square
    with dissolve
    show oren neutral at portrait_left
    with dissolve
    story "Steam leaked from the well in weak white breaths."
    oren "If the water below is this hot, the fields never had a chance."
    return

label anozira_overview_villager:
    scene bg village square
    with dissolve
    show villager neutral at portrait_left
    show oren neutral at portrait_right
    with dissolve
    villager "The Moglim wait where the ground stays warm, even before sunrise."
    oren "Then the heat is choosing its path before we see it."
    return
```

End `label anozira_evening_interlude:` by unlocking the mine:

```renpy
    $ visited_tavern = True
    $ tavern_completed = True
    $ mine_unlocked = True

    story "When dawn finally reached Anozira, the mine route was no longer a guess. It was the only place left for the heat to be hiding."
```

Set the tavern hotspot leave gate in `trailblazers_trials/game/hotspot_scene_data.py`:

```python
            {
                "id": "leave_tavern",
                "marker": "GO",
                "short_label": "Embrum",
                "title": "Finish the tavern scene and regroup with Embrum",
                "x": 1270,
                "y": 210,
                "target": "leave_tavern",
                "requires": ["heard_dead_miner_hint"],
            },
```

- [ ] **Step 4: Re-run the Chapter 1 flow tests and verify the tavern gate passes**

Run:

```bash
python3 -m unittest trailblazers_trials.tests.test_chapter_01_flow -v
```

Expected:

```text
OK
```

- [ ] **Step 5: Commit the mandatory tavern progression**

```bash
git add \
  trailblazers_trials/game/chapters/chapter_01.rpy \
  trailblazers_trials/game/hotspot_scene_data.py \
  trailblazers_trials/tests/test_chapter_01_flow.py
git commit -m "feat: make tavern mandatory before Ruzen mine"
```

### Task 4: Build the first-person tavern investigation hotspot shell

**Files:**
- Modify: `trailblazers_trials/game/systems/exploration.rpy`
- Modify: `trailblazers_trials/game/chapters/chapter_01.rpy`
- Test: `trailblazers_trials/tests/test_hotspot_scene_model.py`

- [ ] **Step 1: Add a failing test that verifies the tavern scene exposes the intended talk targets**

Append to `trailblazers_trials/tests/test_hotspot_scene_model.py`:

```python
    def test_tavern_room_contains_first_person_conversation_targets(self):
        scene = HOTSPOT_SCENES["tavern_room"]
        hotspot_ids = [hotspot["id"] for hotspot in scene["hotspots"]]

        self.assertEqual(
            hotspot_ids,
            ["drunk_father", "wounded_miner", "leave_tavern"],
        )
```

- [ ] **Step 2: Run the hotspot scene tests to verify the tavern scene order does not yet match the new expectation**

Run:

```bash
python3 -m unittest trailblazers_trials.tests.test_hotspot_scene_model -v
```

Expected:

```text
FAIL: test_tavern_room_contains_first_person_conversation_targets
AssertionError: Lists differ: ['wounded_miner', 'drunk_father', 'leave_tavern'] != ['drunk_father', 'wounded_miner', 'leave_tavern']
```

- [ ] **Step 3: Add a generic hotspot scene label and use it for the tavern night scene**

Modify `trailblazers_trials/game/systems/exploration.rpy` by adding:

```renpy
label hotspot_scene_select(scene_id):

    $ exploration_begin(scene_id, reset_position=True)
    call screen exploration_screen
    return _return
```

Refactor `label anozira_evening_interlude:` in `trailblazers_trials/game/chapters/chapter_01.rpy`:

```renpy
    while True:
        $ exploration_map_id = "tavern_room"
        call screen exploration_screen
        $ tavern_choice = _return

        if tavern_choice == "drunk_father":
            call tavern_talk_drunk_father
        elif tavern_choice == "wounded_miner":
            call tavern_talk_wounded_miner
        elif tavern_choice == "leave_tavern":
            jump tavern_finish_night
```

Create the two tavern talk labels:

```renpy
label tavern_talk_drunk_father:
    scene bg tavern first person
    show drunk_father neutral at portrait_left
    show oren neutral at portrait_right
    with dissolve
    drunk_father "Ruzen takes sons. Always did. But it used to give the bodies back."
    oren "Brann was yours."
    drunk_father "Aye. And the mountain still keeps him."
    $ heard_dead_miner_hint = True
    return

label tavern_talk_wounded_miner:
    scene bg tavern first person
    show wounded_miner neutral at portrait_left
    show embrum neutral at portrait_right
    with dissolve
    wounded_miner "If you go to Ruzen, do not trust the quiet."
    embrum "You were inside when it changed?"
    wounded_miner "Close enough to hear stone hiss before flame learned to turn."
    return

label tavern_finish_night:
    scene bg village square night
    with fade
    show embrum neutral at portrait_right
    with dissolve
    embrum "That is enough for tonight. We go at first light, and we go with clearer eyes than fear would give us."
    return
```

- [ ] **Step 4: Re-run the hotspot scene tests**

Run:

```bash
python3 -m unittest trailblazers_trials.tests.test_hotspot_scene_model -v
```

Expected:

```text
OK
```

- [ ] **Step 5: Commit the tavern hotspot scene**

```bash
git add \
  trailblazers_trials/game/systems/exploration.rpy \
  trailblazers_trials/game/chapters/chapter_01.rpy \
  trailblazers_trials/tests/test_hotspot_scene_model.py
git commit -m "feat: add first-person tavern hotspot scene"
```

### Task 5: Replace the plain menu battle preview with a hotspot-based choice battle

**Files:**
- Modify: `trailblazers_trials/game/systems/simple_battle.rpy`
- Modify: `trailblazers_trials/game/hotspot_scene_data.py`
- Modify: `trailblazers_trials/game/variables.rpy`
- Test: `trailblazers_trials/tests/test_chapter_01_flow.py`

- [ ] **Step 1: Write the failing test for the first three-outcome choice battle**

Append to `trailblazers_trials/tests/test_chapter_01_flow.py`:

```python
    def test_choice_battle_scene_contains_three_resolution_targets(self):
        scene = HOTSPOT_SCENES["moglim_water_cart_action"]
        hotspot_ids = [hotspot["id"] for hotspot in scene["hotspots"]]

        self.assertEqual(
            hotspot_ids,
            ["shell", "path", "cart_wheels"],
        )
```

- [ ] **Step 2: Run the Chapter 1 flow tests and confirm the action scene is still missing**

Run:

```bash
python3 -m unittest trailblazers_trials.tests.test_chapter_01_flow -v
```

Expected:

```text
ERROR: KeyError: 'moglim_water_cart_action'
```

- [ ] **Step 3: Add the action scene config and refactor the battle label**

Append to `trailblazers_trials/game/hotspot_scene_data.py`:

```python
    "moglim_water_cart_action": {
        "id": "moglim_water_cart_action",
        "background": "bg nairn fields day",
        "title": "Stop the speeding Moglim",
        "objective": "Choose what Oren aims for before the creature slams into the water cart.",
        "hotspots": [
            {
                "id": "shell",
                "marker": "STRIKE",
                "short_label": "Shell",
                "title": "Hit the heated shell directly",
                "x": 820,
                "y": 470,
                "target": "shell",
            },
            {
                "id": "path",
                "marker": "WATCH",
                "short_label": "Path",
                "title": "Read the Moglim's path and redirect it",
                "x": 615,
                "y": 560,
                "target": "path",
            },
            {
                "id": "cart_wheels",
                "marker": "PULSE",
                "short_label": "Cart",
                "title": "Blast the cart wheels to move the barrels clear",
                "x": 1120,
                "y": 530,
                "target": "cart_wheels",
            },
        ],
    },
```

Replace the plain menu in `trailblazers_trials/game/systems/simple_battle.rpy`:

```renpy
label simple_battle_preview:

    $ exploration_map_id = "moglim_water_cart_action"
    call screen exploration_screen
    $ action_choice = _return

    if action_choice == "path":
        $ village_reputation += 1
        $ embrum_trust += 1
        $ chapter_01_result = "studied"
        story "Oren watched the Moglim's line, stepped aside, and knocked it off the hot groove it had chosen toward the cart."
    elif action_choice == "shell":
        $ oren_resolve += 1
        $ chapter_01_result = "restrained"
        story "Oren struck the shell cleanly, but the burst of heat still sent one barrel cracking across the field."
    elif action_choice == "cart_wheels":
        $ dragon_pressure += 1
        $ qana_strain += 1
        $ chapter_01_result = "voice"
        story "The barrels survived, but Oren's rushed pulse split the cart axle and scorched the ground under it."

    return
```

- [ ] **Step 4: Re-run the Chapter 1 flow tests**

Run:

```bash
python3 -m unittest trailblazers_trials.tests.test_chapter_01_flow -v
```

Expected:

```text
OK
```

- [ ] **Step 5: Commit the hotspot-based choice battle**

```bash
git add \
  trailblazers_trials/game/systems/simple_battle.rpy \
  trailblazers_trials/game/hotspot_scene_data.py \
  trailblazers_trials/game/variables.rpy \
  trailblazers_trials/tests/test_chapter_01_flow.py
git commit -m "feat: add hotspot-based chapter 1 choice battle"
```

### Task 6: Final verification and cleanup

**Files:**
- Modify: `trailblazers_trials/game/data/asset_manifest.md`
- Modify: `trailblazers_trials/docs/STORY_NOTES.md`
- Test: `trailblazers_trials/tests/test_hotspot_scene_model.py`
- Test: `trailblazers_trials/tests/test_chapter_01_flow.py`
- Test: `trailblazers_trials/tests/test_exploration_model.py`

- [ ] **Step 1: Update asset and story notes for the new Chapter 1 structure**

Add to `trailblazers_trials/game/data/asset_manifest.md`:

```markdown
## Chapter 1 Hotspot Scenes

- `images/exploration/anozira_village_backdrop.png`: current Anozira overview backdrop, treated as temporary until a final 16:9 replacement arrives.
- `images/backgrounds/tavern_night.png`: current tavern hotspot backdrop, treated as temporary until a final 16:9 first-person replacement arrives.
```

Add to `trailblazers_trials/docs/STORY_NOTES.md`:

```markdown
- Chapter 1 now uses a day -> tavern night -> mine morning flow.
- The mine route is intentionally locked until the tavern scene completes.
- First-person hotspot scenes and action-targeting scenes now share the same marker system as overview maps.
```

- [ ] **Step 2: Run the focused test files**

Run:

```bash
python3 -m unittest \
  trailblazers_trials.tests.test_hotspot_scene_model \
  trailblazers_trials.tests.test_chapter_01_flow \
  trailblazers_trials.tests.test_exploration_model -v
```

Expected:

```text
OK
```

- [ ] **Step 3: Run the full suite and Ren'Py lint**

Run:

```bash
python3 -m unittest discover -s '/Users/murks/Documents/Codex/2026-04-20-writing-a-novel-game-universe-and/trailblazers_trials/tests' -v
python3 -m compileall '/Users/murks/Documents/Codex/2026-04-20-writing-a-novel-game-universe-and/trailblazers_trials/game'
'/Users/murks/Web-Projects/renpy-8.5.2-sdk/renpy.sh' '/Users/murks/Documents/Codex/2026-04-20-writing-a-novel-game-universe-and/trailblazers_trials' lint
```

Expected:

```text
OK
Lint is not an error, but warnings should still be reviewed.
```

- [ ] **Step 4: Commit the docs and verification pass**

```bash
git add \
  trailblazers_trials/game/data/asset_manifest.md \
  trailblazers_trials/docs/STORY_NOTES.md
git commit -m "docs: record chapter 1 hotspot flow polish"
```
