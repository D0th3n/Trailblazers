# Trailblazers Launcher Design

## Goal

Create a lightweight, professional launcher for Trailblazers that lets players install, update, and play the Ren'Py game on Windows and macOS without cloning the GitHub repository, installing Ren'Py, or using Terminal.

The launcher should feel like a small classic PC game launcher: branded, direct, and useful. It should not become a heavy always-online platform.

## Scope

This design covers:

- a Windows launcher build
- a macOS launcher build
- a public release manifest hosted from the Trailblazers GitHub repository
- manual update checking from inside the launcher
- reinstall-time update checking through the installer/package flow
- local install metadata so the launcher knows the installed game version
- a clear separation between the launcher and the Ren'Py game build

This design does not cover:

- automatic background updates on every launch
- user accounts
- paid distribution
- telemetry
- cloud saves
- multiplayer or online services
- a custom patch-diff system
- native code signing or notarization as a first milestone

## Product Behavior

The player downloads a launcher package for their platform:

- `TrailblazersLauncher-Windows.zip`
- `TrailblazersLauncher-macOS.zip`

When opened, the launcher shows:

- Trailblazers title/logo area
- installed game version
- latest known version, after a manual check
- patch notes summary
- `Play`
- `Check for Updates`
- `Repair / Reinstall`
- optional link to report an issue

The launcher should not check the network every time it opens. It checks for updates only when:

- the player clicks `Check for Updates`
- the player clicks `Repair / Reinstall`
- a future installer/reinstaller runs a setup-time update check

## Update Model

Trailblazers game builds are published as GitHub Release assets. The launcher downloads public release files, not repository source files.

Each release should include platform-specific game archives:

```text
Trailblazers-0.1.1-win.zip
Trailblazers-0.1.1-mac.zip
release-manifest.json
```

The public manifest tells the launcher:

- latest version
- release notes
- platform-specific download URLs
- expected archive filenames
- optional checksums
- minimum launcher version, for future compatibility checks

Example manifest shape:

```json
{
  "gameId": "trailblazers-trials",
  "latestVersion": "0.1.1",
  "releaseNotes": [
    "Expanded Chapter 1 investigation flow.",
    "Added updated Anozira assets."
  ],
  "minimumLauncherVersion": "0.1.0",
  "platforms": {
    "windows": {
      "archive": "Trailblazers-0.1.1-win.zip",
      "url": "https://github.com/D0th3n/Trailblazers/releases/download/v0.1.1/Trailblazers-0.1.1-win.zip",
      "sha256": ""
    },
    "macos": {
      "archive": "Trailblazers-0.1.1-mac.zip",
      "url": "https://github.com/D0th3n/Trailblazers/releases/download/v0.1.1/Trailblazers-0.1.1-mac.zip",
      "sha256": ""
    }
  }
}
```

## Install Layout

The launcher owns a local install folder and keeps the Ren'Py game build inside it.

Recommended install layout:

```text
TrailblazersLauncher/
  launcher/
  game/
    current/
      Trailblazers executable/app bundle
    downloads/
    install-state.json
```

`install-state.json` stores:

- installed version
- platform
- install timestamp
- last manual update check timestamp
- path to current playable executable

The launcher should replace `game/current/` only after a new archive downloads and extracts successfully. If an update fails, the old playable build remains untouched.

## Technical Approach

Use a small Tauri launcher as the preferred implementation.

Reasons:

- cross-platform Windows and macOS support
- much lighter than Electron
- native file/download/process access
- simple web-based UI for branding and layout
- good fit for a small game launcher

The launcher UI can be implemented with a minimal HTML/CSS/TypeScript frontend. It should not need a large frontend framework for the first version.

The launcher backend handles:

- reading local install metadata
- fetching the release manifest
- downloading the platform archive
- extracting the archive
- updating `install-state.json`
- launching the current Ren'Py executable/app

## Data Flow

Manual update check:

1. Player clicks `Check for Updates`.
2. Launcher fetches `release-manifest.json`.
3. Launcher detects the current platform.
4. Launcher compares `latestVersion` with `install-state.json`.
5. If an update exists, launcher asks the player to download it.
6. Launcher downloads the platform archive into `game/downloads/`.
7. Launcher verifies checksum when available.
8. Launcher extracts into a temporary folder.
9. Launcher swaps the temporary folder into `game/current/`.
10. Launcher updates `install-state.json`.

Play:

1. Player clicks `Play`.
2. Launcher reads `install-state.json`.
3. Launcher starts the platform-specific Ren'Py executable or macOS app bundle.
4. Launcher may stay open or close after launching; first version should stay open for easier debugging.

Repair / reinstall:

1. Player clicks `Repair / Reinstall`.
2. Launcher downloads the latest archive even if versions match.
3. Launcher replaces `game/current/` after successful extraction.

## Error Handling

The launcher should show plain, useful messages for:

- no internet connection
- manifest unavailable
- no build for the current platform
- download interrupted
- archive extraction failure
- checksum mismatch
- game executable missing after install

For failures during update or repair, the existing installed game remains playable when possible.

## Release Workflow

Development release process:

1. Build/export the Ren'Py game for Windows and macOS.
2. Name archives with the game version.
3. Update `release-manifest.json`.
4. Create a GitHub Release, such as `v0.1.1`.
5. Upload the Windows archive, macOS archive, and manifest.
6. Test the launcher update flow on both platforms.

The source repository remains useful for development, but testers only need the launcher package.

## Testing Strategy

Unit tests should cover:

- version comparison
- manifest parsing
- platform selection
- install-state read/write
- update availability decisions

Manual release tests should cover:

- fresh install on Windows
- fresh install on macOS
- manual update from an older version
- repair/reinstall when already current
- launch after update
- failed download leaves previous install intact

## First Milestone

The first launcher milestone should be:

- a Tauri app shell named Trailblazers Launcher
- local install-state detection
- manifest fetch from a configurable URL
- manual `Check for Updates`
- download and extract latest platform build
- `Play` button for the installed Ren'Py build
- simple patch notes display

This milestone can ship without auto-updating the launcher itself. Launcher self-update can be added later if the launcher changes frequently enough to justify the added complexity.
