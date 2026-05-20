# Trailblazers Launcher

Trailblazers Launcher is a lightweight Windows/macOS launcher for installing,
updating, repairing, and playing packaged Trailblazers Ren'Py builds.

The current launcher includes a Tauri UI/backend shell, install-state handling,
manifest download support, archive verification, install/repair commands, and
game launching for local packaged builds.

## Development Requirements

- Node.js 24 or newer for UI helper tests
- Python 3 for release manifest generation tests
- Rust through rustup for backend tests
- Tauri CLI 2 through Cargo for launcher development runs

## Test

```bash
./launcher/scripts/test.sh
```

The script runs the UI helper tests, release manifest generator tests, and Rust
backend tests when Cargo is available.

## Development Run

```bash
./launcher/scripts/dev.sh
```

The development run script starts the Tauri launcher against the static UI in
`launcher/ui/`.

## Release Model

Game builds are published as GitHub Release assets. The launcher reads
`release-manifest.json` from the latest release and downloads the correct
platform archive when the player manually checks for updates or runs
repair/reinstall.

The release manifest records the game id, latest game version, release notes,
minimum launcher version, and platform-specific archive URL/checksum entries.

## Prepare Release Manifest

After building the Windows and macOS Ren'Py archives, generate the manifest with:

```bash
python3 launcher/scripts/prepare_release.py \
  --version 0.1.1 \
  --windows-archive dist/Trailblazers-0.1.1-win.zip \
  --macos-archive dist/Trailblazers-0.1.1-mac.zip \
  --note "Expanded Chapter 1 investigation flow." \
  --note "Added updated Anozira assets." \
  --output release-manifest.json
```

Upload the two archives and generated `release-manifest.json` to the matching
GitHub Release, for example `v0.1.1`.
