# Trailblazers Launcher Release Workflow

This workflow packages the Ren'Py game, publishes the versioned archives to a
GitHub Release, and verifies that the launcher can install, update, repair, and
play the release build.

## Build the Ren'Py Game

Use the local Ren'Py SDK app:

`/Users/murks/Web-Projects/renpy-8.5.2-sdk/renpy.app`

Use this repository family as the Ren'Py projects directory:

`/Users/murks/Library/Mobile Documents/.Trash/Codex/2026-04-20-writing-a-novel-game-universe-and`

Build steps:

1. Open the Ren'Py SDK app.
2. Set the projects directory to the path above.
3. Select the `trailblazers_trials` project.
4. Choose the distribution/build option.
5. Build Windows and macOS packages for version `0.1.1`.
6. Confirm the packaged archives are named:
   - `Trailblazers-0.1.1-win.zip`
   - `Trailblazers-0.1.1-mac.zip`

## Prepare Release Assets

Create or update `release-manifest.json` so the launcher can discover version
`0.1.1` and download the correct platform archive. The manifest should point to
the uploaded GitHub Release asset URLs for:

- `Trailblazers-0.1.1-win.zip`
- `Trailblazers-0.1.1-mac.zip`

Before publishing, confirm the manifest includes the expected game id, latest
game version, release notes, minimum launcher version, platform archive URLs, and
archive checksums.

## Publish GitHub Release `v0.1.1`

1. Create a GitHub Release tagged `v0.1.1`.
2. Use concise release notes that match the `release-manifest.json` notes.
3. Upload these assets to the release:
   - `Trailblazers-0.1.1-win.zip`
   - `Trailblazers-0.1.1-mac.zip`
   - `release-manifest.json`
4. After upload, verify each asset can be downloaded from the release page.
5. Confirm the manifest archive URLs match the final release asset URLs.

## Launcher Update Test Checklist

Run this checklist on Windows and macOS whenever possible:

- Start with no installed Trailblazers build and open the launcher.
- Use `Check for Updates` and confirm version `0.1.1` is discovered.
- Install the build and confirm the launcher reports the installed version.
- Use `Play` and confirm the packaged Ren'Py game starts.
- Close the game and return to the launcher.
- Use `Repair / Reinstall` and confirm the launcher redownloads or reinstalls
  the same release without losing the ability to launch.
- Use `Play` again after repair and confirm the game starts.
- If an older local build is available, install it first, then use
  `Check for Updates` to verify the launcher offers `0.1.1`.
