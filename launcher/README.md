# Trailblazers Launcher

Trailblazers Launcher is a lightweight Windows/macOS launcher for installing,
updating, repairing, and playing packaged Trailblazers Ren'Py builds.

This first slice contains the static UI shell and pure JavaScript helper tests.
The Rust/Tauri backend will provide filesystem, download, install-state, and
game-launching commands in a later task.

## Development Requirements

- Node.js 24 or newer for UI helper tests
- Rust through rustup for future backend tests
- Tauri CLI 2 through Cargo for future launcher development runs

## Test

```bash
./launcher/scripts/test.sh
```

The script runs the static UI helper tests. It also runs Rust tests when Cargo
is available and `launcher/src-tauri` has been added.

## Development Run

```bash
./launcher/scripts/dev.sh
```

The development run script will be added with the Tauri backend. Once present,
it should start the launcher against the static UI in `launcher/ui/`.

## Release Model

Game builds are published as GitHub Release assets. The launcher reads
`release-manifest.json` from the latest release and downloads the correct
platform archive when the player manually checks for updates or runs
repair/reinstall.

The release manifest records the game id, latest game version, release notes,
minimum launcher version, and platform-specific archive URL/checksum entries.
