# Trailblazers Launcher Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first Windows/macOS Trailblazers Launcher milestone with manual update checking, repair/reinstall, and a Play button for packaged Ren'Py builds.

**Architecture:** Add a separate `launcher/` app at the repository root. Use a static HTML/CSS/JavaScript UI for the visible launcher and a Rust/Tauri backend for filesystem, download, extraction, install-state, and process launching. Keep Ren'Py game source and launcher code separate so game builds can be updated without rebuilding launcher code every time.

**Tech Stack:** Tauri 2, Rust, static HTML/CSS/JavaScript, Node's built-in test runner for UI helpers, Rust unit tests for backend helpers, GitHub Releases for release assets and `release-manifest.json`.

---

## File Structure

- `launcher/README.md`
  - Explains local launcher setup, build commands, and release workflow.
- `launcher/release-manifest.example.json`
  - Example manifest shape for GitHub Releases.
- `launcher/scripts/dev.sh`
  - Starts the Tauri launcher in development mode after checking the Rust/Tauri toolchain.
- `launcher/scripts/test.sh`
  - Runs JavaScript helper tests and Rust backend tests.
- `launcher/ui/index.html`
  - Static launcher UI shell.
- `launcher/ui/styles.css`
  - Branded Trailblazers launcher styling.
- `launcher/ui/launcher-state.js`
  - Pure JavaScript helpers for status text, version comparison display, and platform labels.
- `launcher/ui/launcher-state.test.mjs`
  - Node tests for pure UI helper behavior.
- `launcher/ui/app.js`
  - Browser-side launcher controller that calls Tauri commands.
- `launcher/src-tauri/Cargo.toml`
  - Rust package configuration and dependencies.
- `launcher/src-tauri/build.rs`
  - Tauri build hook.
- `launcher/src-tauri/tauri.conf.json`
  - Tauri app configuration.
- `launcher/src-tauri/src/main.rs`
  - Tauri entrypoint.
- `launcher/src-tauri/src/lib.rs`
  - Registers commands and shared state.
- `launcher/src-tauri/src/manifest.rs`
  - Manifest structs, platform selection, and version comparison.
- `launcher/src-tauri/src/install_state.rs`
  - Install state read/write and launcher-owned path layout.
- `launcher/src-tauri/src/installer.rs`
  - Download, checksum, extraction, atomic replacement, and repair/reinstall flow.
- `launcher/src-tauri/src/launcher.rs`
  - Platform-specific Ren'Py executable/app launch logic.
- `.gitignore`
  - Ignore launcher build output and downloaded game archives.

## Toolchain Setup

### Task 1: Install and Verify the Launcher Toolchain

**Files:**
- No repository files changed.

- [ ] **Step 1: Install Rust**

Run:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Expected:

```text
Rust is installed now.
```

- [ ] **Step 2: Restart the terminal shell or load Cargo env**

Run:

```bash
source "$HOME/.cargo/env"
```

Expected: no output.

- [ ] **Step 3: Install the Tauri CLI**

Run:

```bash
cargo install tauri-cli --version "^2"
```

Expected:

```text
Installed package `tauri-cli`
```

- [ ] **Step 4: Verify the required commands**

Run:

```bash
node --version
cargo --version
rustc --version
cargo tauri --version
```

Expected:

```text
v24...
cargo ...
rustc ...
tauri-cli ...
```

## Static UI Foundation

### Task 2: Add the Static Launcher UI and UI Helper Tests

**Files:**
- Create: `launcher/README.md`
- Create: `launcher/release-manifest.example.json`
- Create: `launcher/scripts/test.sh`
- Create: `launcher/ui/index.html`
- Create: `launcher/ui/styles.css`
- Create: `launcher/ui/launcher-state.js`
- Create: `launcher/ui/launcher-state.test.mjs`
- Modify: `.gitignore`

- [ ] **Step 1: Write the UI helper test**

Create `launcher/ui/launcher-state.test.mjs`:

```javascript
import test from "node:test";
import assert from "node:assert/strict";
import {
  formatInstalledVersion,
  formatLatestVersion,
  isUpdateAvailable,
  platformLabel,
} from "./launcher-state.js";

test("formatInstalledVersion describes missing installs", () => {
  assert.equal(formatInstalledVersion(null), "Not installed");
  assert.equal(formatInstalledVersion({ installedVersion: "" }), "Not installed");
});

test("formatInstalledVersion shows installed version", () => {
  assert.equal(
    formatInstalledVersion({ installedVersion: "0.1.1" }),
    "Installed: 0.1.1",
  );
});

test("formatLatestVersion shows unchecked state and manifest version", () => {
  assert.equal(formatLatestVersion(null), "Latest: not checked");
  assert.equal(formatLatestVersion({ latestVersion: "0.1.2" }), "Latest: 0.1.2");
});

test("isUpdateAvailable compares semantic numeric parts", () => {
  assert.equal(isUpdateAvailable("0.1.0", "0.1.1"), true);
  assert.equal(isUpdateAvailable("0.1.9", "0.1.10"), true);
  assert.equal(isUpdateAvailable("0.2.0", "0.1.10"), false);
  assert.equal(isUpdateAvailable("0.1.1", "0.1.1"), false);
});

test("platformLabel normalizes backend platform identifiers", () => {
  assert.equal(platformLabel("windows"), "Windows");
  assert.equal(platformLabel("macos"), "macOS");
  assert.equal(platformLabel("linux"), "Linux");
});
```

- [ ] **Step 2: Run the UI helper test to verify it fails**

Run:

```bash
node --test launcher/ui/launcher-state.test.mjs
```

Expected:

```text
ERR_MODULE_NOT_FOUND
```

- [ ] **Step 3: Add UI helper implementation**

Create `launcher/ui/launcher-state.js`:

```javascript
export function formatInstalledVersion(state) {
  if (!state || !state.installedVersion) {
    return "Not installed";
  }
  return `Installed: ${state.installedVersion}`;
}

export function formatLatestVersion(manifest) {
  if (!manifest || !manifest.latestVersion) {
    return "Latest: not checked";
  }
  return `Latest: ${manifest.latestVersion}`;
}

export function versionParts(version) {
  return String(version)
    .split(".")
    .map((part) => Number.parseInt(part, 10))
    .map((part) => (Number.isFinite(part) ? part : 0));
}

export function isUpdateAvailable(installedVersion, latestVersion) {
  const installed = versionParts(installedVersion);
  const latest = versionParts(latestVersion);
  const length = Math.max(installed.length, latest.length);

  for (let index = 0; index < length; index += 1) {
    const installedPart = installed[index] || 0;
    const latestPart = latest[index] || 0;
    if (latestPart > installedPart) {
      return true;
    }
    if (latestPart < installedPart) {
      return false;
    }
  }

  return false;
}

export function platformLabel(platform) {
  if (platform === "windows") {
    return "Windows";
  }
  if (platform === "macos") {
    return "macOS";
  }
  if (platform === "linux") {
    return "Linux";
  }
  return "Unknown platform";
}
```

- [ ] **Step 4: Add launcher HTML**

Create `launcher/ui/index.html`:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Trailblazers Launcher</title>
    <link rel="stylesheet" href="./styles.css" />
  </head>
  <body>
    <main class="launcher-shell">
      <section class="hero">
        <div>
          <p class="eyebrow">Trailblazers Trials</p>
          <h1>Trailblazers Launcher</h1>
          <p class="subtitle">Install, update, and play the current test build.</p>
        </div>
        <div class="version-panel" aria-label="Version information">
          <p id="platformLabel">Platform: detecting...</p>
          <p id="installedVersion">Not installed</p>
          <p id="latestVersion">Latest: not checked</p>
        </div>
      </section>

      <section class="actions" aria-label="Launcher actions">
        <button id="playButton" type="button">Play</button>
        <button id="checkButton" type="button">Check for Updates</button>
        <button id="repairButton" type="button">Repair / Reinstall</button>
      </section>

      <section class="status-area" aria-live="polite">
        <h2>Status</h2>
        <p id="statusText">Ready.</p>
      </section>

      <section class="notes-area">
        <h2>Patch Notes</h2>
        <ul id="patchNotes">
          <li>Check for updates to load the latest release notes.</li>
        </ul>
      </section>
    </main>

    <script type="module" src="./app.js"></script>
  </body>
</html>
```

- [ ] **Step 5: Add launcher CSS**

Create `launcher/ui/styles.css`:

```css
:root {
  color: #f8efe4;
  background: #160f0b;
  font-family:
    Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
    sans-serif;
}

* {
  box-sizing: border-box;
}

body {
  min-height: 100vh;
  margin: 0;
  background:
    linear-gradient(135deg, rgba(48, 22, 10, 0.72), rgba(9, 15, 20, 0.92)),
    #160f0b;
}

button {
  min-height: 44px;
  border: 1px solid #d89742;
  border-radius: 6px;
  padding: 0 18px;
  color: #1d130d;
  background: #f2b35b;
  font: inherit;
  font-weight: 700;
  cursor: pointer;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.launcher-shell {
  width: min(920px, calc(100vw - 40px));
  margin: 0 auto;
  padding: 44px 0;
}

.hero {
  display: grid;
  grid-template-columns: 1fr minmax(220px, 300px);
  gap: 24px;
  align-items: end;
  padding-bottom: 28px;
  border-bottom: 1px solid rgba(248, 239, 228, 0.18);
}

.eyebrow {
  margin: 0 0 8px;
  color: #f2b35b;
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
}

h1,
h2,
p {
  margin-top: 0;
}

h1 {
  margin-bottom: 10px;
  font-size: 44px;
  line-height: 1.02;
}

h2 {
  margin-bottom: 10px;
  color: #f7dcb8;
  font-size: 18px;
}

.subtitle {
  max-width: 520px;
  margin-bottom: 0;
  color: #e7d2bd;
}

.version-panel,
.status-area,
.notes-area {
  border: 1px solid rgba(248, 239, 228, 0.18);
  border-radius: 8px;
  background: rgba(19, 13, 10, 0.72);
  padding: 18px;
}

.version-panel p,
.status-area p {
  margin-bottom: 6px;
  color: #f8efe4;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  padding: 24px 0;
}

.notes-area ul {
  margin: 0;
  padding-left: 20px;
  color: #ead8c7;
}

@media (max-width: 720px) {
  .hero {
    grid-template-columns: 1fr;
  }

  h1 {
    font-size: 34px;
  }
}
```

- [ ] **Step 6: Add initial browser controller**

Create `launcher/ui/app.js`:

```javascript
import {
  formatInstalledVersion,
  formatLatestVersion,
  isUpdateAvailable,
  platformLabel,
} from "./launcher-state.js";

const DEFAULT_MANIFEST_URL =
  "https://github.com/D0th3n/Trailblazers/releases/latest/download/release-manifest.json";

const tauriInvoke = window.__TAURI__?.core?.invoke;

const elements = {
  platformLabel: document.querySelector("#platformLabel"),
  installedVersion: document.querySelector("#installedVersion"),
  latestVersion: document.querySelector("#latestVersion"),
  playButton: document.querySelector("#playButton"),
  checkButton: document.querySelector("#checkButton"),
  repairButton: document.querySelector("#repairButton"),
  statusText: document.querySelector("#statusText"),
  patchNotes: document.querySelector("#patchNotes"),
};

let installState = null;
let latestManifest = null;

function setStatus(message) {
  elements.statusText.textContent = message;
}

function setButtons(disabled) {
  elements.playButton.disabled = disabled;
  elements.checkButton.disabled = disabled;
  elements.repairButton.disabled = disabled;
}

function renderPatchNotes(notes) {
  elements.patchNotes.innerHTML = "";
  const list = notes && notes.length ? notes : ["No release notes loaded."];
  for (const note of list) {
    const item = document.createElement("li");
    item.textContent = note;
    elements.patchNotes.append(item);
  }
}

function render() {
  elements.platformLabel.textContent = `Platform: ${platformLabel(installState?.platform)}`;
  elements.installedVersion.textContent = formatInstalledVersion(installState);
  elements.latestVersion.textContent = formatLatestVersion(latestManifest);
  renderPatchNotes(latestManifest?.releaseNotes);

  const installed = installState?.installedVersion;
  const latest = latestManifest?.latestVersion;
  if (installed && latest && isUpdateAvailable(installed, latest)) {
    setStatus(`Update available: ${latest}.`);
  }
}

async function invoke(command, args = {}) {
  if (!tauriInvoke) {
    throw new Error("Tauri API is unavailable. Run this UI through the launcher app.");
  }
  return tauriInvoke(command, args);
}

async function loadInstallState() {
  installState = await invoke("read_install_state");
  render();
}

async function checkForUpdates() {
  setButtons(true);
  setStatus("Checking for updates...");
  try {
    latestManifest = await invoke("check_for_updates", {
      manifestUrl: DEFAULT_MANIFEST_URL,
    });
    render();
    setStatus("Update check complete.");
  } catch (error) {
    setStatus(`Update check failed: ${error}`);
  } finally {
    setButtons(false);
  }
}

async function repairOrReinstall() {
  setButtons(true);
  setStatus("Downloading latest build...");
  try {
    installState = await invoke("install_latest", {
      manifestUrl: DEFAULT_MANIFEST_URL,
      force: true,
    });
    await checkForUpdates();
    setStatus("Repair / reinstall complete.");
  } catch (error) {
    setStatus(`Repair / reinstall failed: ${error}`);
  } finally {
    setButtons(false);
  }
}

async function playGame() {
  setButtons(true);
  setStatus("Launching Trailblazers...");
  try {
    await invoke("launch_game");
    setStatus("Game launched.");
  } catch (error) {
    setStatus(`Launch failed: ${error}`);
  } finally {
    setButtons(false);
  }
}

elements.checkButton.addEventListener("click", checkForUpdates);
elements.repairButton.addEventListener("click", repairOrReinstall);
elements.playButton.addEventListener("click", playGame);

loadInstallState().catch((error) => {
  setStatus(`Could not read install state: ${error}`);
});
```

- [ ] **Step 7: Add example release manifest**

Create `launcher/release-manifest.example.json`:

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

- [ ] **Step 8: Add test script**

Create `launcher/scripts/test.sh`:

```bash
#!/bin/zsh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

cd "$REPO_ROOT"
node --test launcher/ui/launcher-state.test.mjs

if command -v cargo >/dev/null 2>&1; then
  cd "$REPO_ROOT/launcher/src-tauri"
  cargo test
else
  echo "cargo not found; Rust tests skipped until the Tauri toolchain is installed."
fi
```

Run:

```bash
chmod +x launcher/scripts/test.sh
```

- [ ] **Step 9: Add launcher README**

Create `launcher/README.md`:

```markdown
# Trailblazers Launcher

Trailblazers Launcher is a lightweight Windows/macOS launcher for installing,
updating, repairing, and playing packaged Trailblazers Ren'Py builds.

## Development Requirements

- Node.js 24 or newer for UI helper tests
- Rust through rustup
- Tauri CLI 2 through Cargo

## Test

```bash
./launcher/scripts/test.sh
```

## Development Run

```bash
./launcher/scripts/dev.sh
```

## Release Model

Game builds are published as GitHub Release assets. The launcher reads
`release-manifest.json` and downloads the correct platform archive when the
player manually checks for updates or runs repair/reinstall.
```

- [ ] **Step 10: Update `.gitignore`**

Append to `.gitignore`:

```gitignore

# Trailblazers launcher build/download output
launcher/src-tauri/target/
launcher/game/
launcher/**/*.log
```

- [ ] **Step 11: Run UI tests**

Run:

```bash
./launcher/scripts/test.sh
```

Expected with Rust missing:

```text
ok
cargo not found; Rust tests skipped until the Tauri toolchain is installed.
```

Expected with Rust installed:

```text
ok
test result: ok
```

- [ ] **Step 12: Commit the UI foundation**

Run:

```bash
git add .gitignore launcher/README.md launcher/release-manifest.example.json launcher/scripts/test.sh launcher/ui
git commit -m "feat: add Trailblazers launcher UI shell"
```

## Tauri Backend Foundation

### Task 3: Add Tauri App Configuration and Backend Models

**Files:**
- Create: `launcher/scripts/dev.sh`
- Create: `launcher/src-tauri/Cargo.toml`
- Create: `launcher/src-tauri/build.rs`
- Create: `launcher/src-tauri/tauri.conf.json`
- Create: `launcher/src-tauri/src/main.rs`
- Create: `launcher/src-tauri/src/lib.rs`
- Create: `launcher/src-tauri/src/manifest.rs`
- Create: `launcher/src-tauri/src/install_state.rs`

- [ ] **Step 1: Add Rust manifest helper tests**

Create `launcher/src-tauri/src/manifest.rs`:

```rust
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

#[derive(Clone, Debug, Deserialize, Serialize, PartialEq, Eq)]
#[serde(rename_all = "camelCase")]
pub struct ReleaseManifest {
    pub game_id: String,
    pub latest_version: String,
    pub release_notes: Vec<String>,
    pub minimum_launcher_version: String,
    pub platforms: BTreeMap<String, PlatformRelease>,
}

#[derive(Clone, Debug, Deserialize, Serialize, PartialEq, Eq)]
pub struct PlatformRelease {
    pub archive: String,
    pub url: String,
    #[serde(default)]
    pub sha256: String,
}

pub fn current_platform() -> &'static str {
    if cfg!(target_os = "windows") {
        "windows"
    } else if cfg!(target_os = "macos") {
        "macos"
    } else {
        "linux"
    }
}

pub fn platform_release<'a>(
    manifest: &'a ReleaseManifest,
    platform: &str,
) -> Result<&'a PlatformRelease, String> {
    manifest
        .platforms
        .get(platform)
        .ok_or_else(|| format!("No Trailblazers build is available for {platform}."))
}

pub fn compare_versions(left: &str, right: &str) -> std::cmp::Ordering {
    let left_parts = version_parts(left);
    let right_parts = version_parts(right);
    let length = left_parts.len().max(right_parts.len());

    for index in 0..length {
        let left_part = *left_parts.get(index).unwrap_or(&0);
        let right_part = *right_parts.get(index).unwrap_or(&0);
        match left_part.cmp(&right_part) {
            std::cmp::Ordering::Equal => {}
            ordering => return ordering,
        }
    }

    std::cmp::Ordering::Equal
}

fn version_parts(version: &str) -> Vec<u32> {
    version
        .split('.')
        .map(|part| part.parse::<u32>().unwrap_or(0))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    fn manifest() -> ReleaseManifest {
        let mut platforms = BTreeMap::new();
        platforms.insert(
            "windows".to_string(),
            PlatformRelease {
                archive: "Trailblazers-0.1.1-win.zip".to_string(),
                url: "https://example.test/win.zip".to_string(),
                sha256: String::new(),
            },
        );

        ReleaseManifest {
            game_id: "trailblazers-trials".to_string(),
            latest_version: "0.1.1".to_string(),
            release_notes: vec!["Patch note".to_string()],
            minimum_launcher_version: "0.1.0".to_string(),
            platforms,
        }
    }

    #[test]
    fn platform_release_returns_matching_build() {
        let release = platform_release(&manifest(), "windows").unwrap();
        assert_eq!(release.archive, "Trailblazers-0.1.1-win.zip");
    }

    #[test]
    fn platform_release_reports_missing_build() {
        let error = platform_release(&manifest(), "macos").unwrap_err();
        assert_eq!(error, "No Trailblazers build is available for macos.");
    }

    #[test]
    fn compare_versions_orders_numeric_parts() {
        assert_eq!(
            compare_versions("0.1.10", "0.1.9"),
            std::cmp::Ordering::Greater
        );
        assert_eq!(
            compare_versions("0.1.0", "0.1.1"),
            std::cmp::Ordering::Less
        );
        assert_eq!(
            compare_versions("0.1.1", "0.1.1"),
            std::cmp::Ordering::Equal
        );
    }
}
```

- [ ] **Step 2: Add install-state tests and implementation**

Create `launcher/src-tauri/src/install_state.rs`:

```rust
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::{Path, PathBuf};

#[derive(Clone, Debug, Deserialize, Serialize, PartialEq, Eq)]
#[serde(rename_all = "camelCase")]
pub struct InstallState {
    pub installed_version: String,
    pub platform: String,
    pub installed_at: String,
    pub last_manual_update_check_at: Option<String>,
    pub executable_path: String,
}

impl InstallState {
    pub fn empty(platform: &str) -> Self {
        Self {
            installed_version: String::new(),
            platform: platform.to_string(),
            installed_at: String::new(),
            last_manual_update_check_at: None,
            executable_path: String::new(),
        }
    }
}

pub fn install_root(app_data_dir: &Path) -> PathBuf {
    app_data_dir.join("TrailblazersLauncher")
}

pub fn state_path(app_data_dir: &Path) -> PathBuf {
    install_root(app_data_dir).join("install-state.json")
}

pub fn current_game_dir(app_data_dir: &Path) -> PathBuf {
    install_root(app_data_dir).join("game").join("current")
}

pub fn downloads_dir(app_data_dir: &Path) -> PathBuf {
    install_root(app_data_dir).join("game").join("downloads")
}

pub fn read_state(app_data_dir: &Path, platform: &str) -> Result<InstallState, String> {
    let path = state_path(app_data_dir);
    if !path.exists() {
        return Ok(InstallState::empty(platform));
    }

    let contents = fs::read_to_string(&path)
        .map_err(|error| format!("Could not read install state: {error}"))?;
    serde_json::from_str(&contents)
        .map_err(|error| format!("Could not parse install state: {error}"))
}

pub fn write_state(app_data_dir: &Path, state: &InstallState) -> Result<(), String> {
    let path = state_path(app_data_dir);
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)
            .map_err(|error| format!("Could not create install state folder: {error}"))?;
    }
    let contents = serde_json::to_string_pretty(state)
        .map_err(|error| format!("Could not serialize install state: {error}"))?;
    fs::write(&path, contents)
        .map_err(|error| format!("Could not write install state: {error}"))
}

pub fn now_iso() -> String {
    let now: DateTime<Utc> = Utc::now();
    now.to_rfc3339()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn empty_state_uses_platform_and_blank_version() {
        let state = InstallState::empty("macos");
        assert_eq!(state.platform, "macos");
        assert_eq!(state.installed_version, "");
    }

    #[test]
    fn path_helpers_keep_game_under_launcher_root() {
        let root = PathBuf::from("/tmp/app-data");
        assert_eq!(
            state_path(&root),
            PathBuf::from("/tmp/app-data/TrailblazersLauncher/install-state.json")
        );
        assert_eq!(
            current_game_dir(&root),
            PathBuf::from("/tmp/app-data/TrailblazersLauncher/game/current")
        );
        assert_eq!(
            downloads_dir(&root),
            PathBuf::from("/tmp/app-data/TrailblazersLauncher/game/downloads")
        );
    }
}
```

- [ ] **Step 3: Add Cargo configuration**

Create `launcher/src-tauri/Cargo.toml`:

```toml
[package]
name = "trailblazers-launcher"
version = "0.1.0"
description = "Trailblazers Launcher"
authors = ["D0th3n"]
edition = "2021"

[lib]
name = "trailblazers_launcher_lib"
crate-type = ["staticlib", "cdylib", "rlib"]

[build-dependencies]
tauri-build = { version = "2", features = [] }

[dependencies]
chrono = { version = "0.4", features = ["serde"] }
reqwest = { version = "0.12", features = ["blocking", "json"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
sha2 = "0.10"
tauri = { version = "2", features = [] }
tempfile = "3"
zip = "2"

[features]
custom-protocol = ["tauri/custom-protocol"]
```

- [ ] **Step 4: Add Tauri config**

Create `launcher/src-tauri/tauri.conf.json`:

```json
{
  "$schema": "https://schema.tauri.app/config/2",
  "productName": "Trailblazers Launcher",
  "version": "0.1.0",
  "identifier": "com.d0th3n.trailblazers.launcher",
  "build": {
    "beforeDevCommand": "",
    "beforeBuildCommand": "",
    "devUrl": "../ui",
    "frontendDist": "../ui"
  },
  "app": {
    "withGlobalTauri": true,
    "windows": [
      {
        "title": "Trailblazers Launcher",
        "width": 980,
        "height": 680,
        "resizable": true
      }
    ],
    "security": {
      "csp": null
    }
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": []
  }
}
```

- [ ] **Step 5: Add Tauri build entrypoints**

Create `launcher/src-tauri/build.rs`:

```rust
fn main() {
    tauri_build::build()
}
```

Create `launcher/src-tauri/src/main.rs`:

```rust
fn main() {
    trailblazers_launcher_lib::run()
}
```

Create `launcher/src-tauri/src/lib.rs`:

```rust
mod install_state;
mod manifest;

use install_state::InstallState;
use manifest::{current_platform, ReleaseManifest};
use tauri::Manager;

#[tauri::command]
fn read_install_state(app: tauri::AppHandle) -> Result<InstallState, String> {
    let app_data = app
        .path()
        .app_data_dir()
        .map_err(|error| format!("Could not resolve app data directory: {error}"))?;
    install_state::read_state(&app_data, current_platform())
}

#[tauri::command]
fn check_for_updates(manifest_url: String) -> Result<ReleaseManifest, String> {
    reqwest::blocking::get(&manifest_url)
        .map_err(|error| format!("Could not fetch release manifest: {error}"))?
        .json::<ReleaseManifest>()
        .map_err(|error| format!("Could not parse release manifest: {error}"))
}

#[tauri::command]
fn install_latest(
    app: tauri::AppHandle,
    manifest_url: String,
    force: bool,
) -> Result<InstallState, String> {
    let _ = force;
    let _ = manifest_url;
    let app_data = app
        .path()
        .app_data_dir()
        .map_err(|error| format!("Could not resolve app data directory: {error}"))?;
    install_state::read_state(&app_data, current_platform())
}

#[tauri::command]
fn launch_game() -> Result<(), String> {
    Err("No installed Trailblazers build was found. Use Repair / Reinstall first.".to_string())
}

pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            read_install_state,
            check_for_updates,
            install_latest,
            launch_game
        ])
        .run(tauri::generate_context!())
        .expect("error while running Trailblazers Launcher");
}
```

- [ ] **Step 6: Add development script**

Create `launcher/scripts/dev.sh`:

```bash
#!/bin/zsh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

if ! command -v cargo >/dev/null 2>&1; then
  echo "cargo not found. Install Rust with rustup before running the launcher."
  exit 1
fi

cd "$REPO_ROOT/launcher/src-tauri"
cargo tauri dev
```

Run:

```bash
chmod +x launcher/scripts/dev.sh
```

- [ ] **Step 7: Run backend tests**

Run:

```bash
cd launcher/src-tauri
cargo test
```

Expected:

```text
test result: ok
```

- [ ] **Step 8: Run all launcher tests**

Run:

```bash
./launcher/scripts/test.sh
```

Expected:

```text
ok
test result: ok
```

- [ ] **Step 9: Commit backend foundation**

Run:

```bash
git add launcher/scripts/dev.sh launcher/src-tauri
git commit -m "feat: add Trailblazers launcher backend shell"
```

## Download and Install Flow

### Task 4: Implement Manifest-Based Download, Verify, and Install

**Files:**
- Create: `launcher/src-tauri/src/installer.rs`
- Modify: `launcher/src-tauri/src/lib.rs`

- [ ] **Step 1: Add installer module tests**

Create `launcher/src-tauri/src/installer.rs`:

```rust
use crate::install_state::{self, InstallState};
use crate::manifest::{compare_versions, current_platform, platform_release, ReleaseManifest};
use sha2::{Digest, Sha256};
use std::fs;
use std::io::{Cursor, Read};
use std::path::{Path, PathBuf};
use zip::ZipArchive;

pub fn update_is_needed(installed: &InstallState, manifest: &ReleaseManifest, force: bool) -> bool {
    if force {
        return true;
    }
    if installed.installed_version.is_empty() {
        return true;
    }
    compare_versions(&manifest.latest_version, &installed.installed_version).is_gt()
}

pub fn verify_sha256(bytes: &[u8], expected: &str) -> Result<(), String> {
    if expected.trim().is_empty() {
        return Ok(());
    }

    let mut hasher = Sha256::new();
    hasher.update(bytes);
    let actual = format!("{:x}", hasher.finalize());
    if actual == expected {
        Ok(())
    } else {
        Err("Downloaded build failed checksum verification.".to_string())
    }
}

pub fn extract_zip(bytes: &[u8], destination: &Path) -> Result<(), String> {
    fs::create_dir_all(destination)
        .map_err(|error| format!("Could not create extraction folder: {error}"))?;

    let reader = Cursor::new(bytes);
    let mut archive =
        ZipArchive::new(reader).map_err(|error| format!("Could not read zip archive: {error}"))?;

    for index in 0..archive.len() {
        let mut file = archive
            .by_index(index)
            .map_err(|error| format!("Could not read zip entry: {error}"))?;
        let output_path = safe_output_path(destination, file.name())?;

        if file.is_dir() {
            fs::create_dir_all(&output_path)
                .map_err(|error| format!("Could not create folder from zip: {error}"))?;
        } else {
            if let Some(parent) = output_path.parent() {
                fs::create_dir_all(parent)
                    .map_err(|error| format!("Could not create zip parent folder: {error}"))?;
            }
            let mut output = fs::File::create(&output_path)
                .map_err(|error| format!("Could not create extracted file: {error}"))?;
            std::io::copy(&mut file, &mut output)
                .map_err(|error| format!("Could not write extracted file: {error}"))?;
        }
    }

    Ok(())
}

fn safe_output_path(destination: &Path, name: &str) -> Result<PathBuf, String> {
    let path = destination.join(name);
    let normalized = path
        .components()
        .try_fold(PathBuf::new(), |mut output, component| {
            match component {
                std::path::Component::ParentDir => Err(()),
                _ => {
                    output.push(component.as_os_str());
                    Ok(output)
                }
            }
        })
        .map_err(|_| "Zip archive contains an unsafe path.".to_string())?;
    Ok(normalized)
}

pub fn fetch_manifest(manifest_url: &str) -> Result<ReleaseManifest, String> {
    reqwest::blocking::get(manifest_url)
        .map_err(|error| format!("Could not fetch release manifest: {error}"))?
        .json::<ReleaseManifest>()
        .map_err(|error| format!("Could not parse release manifest: {error}"))
}

pub fn install_latest_from_manifest(
    app_data_dir: &Path,
    manifest: &ReleaseManifest,
    archive_bytes: &[u8],
    force: bool,
) -> Result<InstallState, String> {
    let platform = current_platform();
    let release = platform_release(manifest, platform)?;
    let installed = install_state::read_state(app_data_dir, platform)?;

    if !update_is_needed(&installed, manifest, force) {
        return Ok(installed);
    }

    verify_sha256(archive_bytes, &release.sha256)?;

    let current_dir = install_state::current_game_dir(app_data_dir);
    let temp_dir = current_dir.with_extension("next");
    if temp_dir.exists() {
        fs::remove_dir_all(&temp_dir)
            .map_err(|error| format!("Could not clear previous temp install: {error}"))?;
    }
    extract_zip(archive_bytes, &temp_dir)?;

    if current_dir.exists() {
        fs::remove_dir_all(&current_dir)
            .map_err(|error| format!("Could not replace previous install: {error}"))?;
    }
    fs::rename(&temp_dir, &current_dir)
        .map_err(|error| format!("Could not activate new install: {error}"))?;

    let executable_path = current_dir.to_string_lossy().to_string();
    let state = InstallState {
        installed_version: manifest.latest_version.clone(),
        platform: platform.to_string(),
        installed_at: install_state::now_iso(),
        last_manual_update_check_at: Some(install_state::now_iso()),
        executable_path,
    };
    install_state::write_state(app_data_dir, &state)?;
    Ok(state)
}

pub fn download_archive(url: &str) -> Result<Vec<u8>, String> {
    let mut response =
        reqwest::blocking::get(url).map_err(|error| format!("Could not download build: {error}"))?;
    let mut bytes = Vec::new();
    response
        .read_to_end(&mut bytes)
        .map_err(|error| format!("Could not read downloaded build: {error}"))?;
    Ok(bytes)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::manifest::{PlatformRelease, ReleaseManifest};
    use std::collections::BTreeMap;

    fn manifest(version: &str) -> ReleaseManifest {
        let mut platforms = BTreeMap::new();
        platforms.insert(
            current_platform().to_string(),
            PlatformRelease {
                archive: "Trailblazers.zip".to_string(),
                url: "https://example.test/Trailblazers.zip".to_string(),
                sha256: String::new(),
            },
        );
        ReleaseManifest {
            game_id: "trailblazers-trials".to_string(),
            latest_version: version.to_string(),
            release_notes: vec!["Patch note".to_string()],
            minimum_launcher_version: "0.1.0".to_string(),
            platforms,
        }
    }

    #[test]
    fn update_is_needed_when_forced_or_missing_or_newer() {
        let mut installed = InstallState::empty(current_platform());
        assert!(update_is_needed(&installed, &manifest("0.1.0"), false));

        installed.installed_version = "0.1.0".to_string();
        assert!(!update_is_needed(&installed, &manifest("0.1.0"), false));
        assert!(update_is_needed(&installed, &manifest("0.1.1"), false));
        assert!(update_is_needed(&installed, &manifest("0.1.0"), true));
    }

    #[test]
    fn blank_checksum_is_accepted() {
        assert!(verify_sha256(b"abc", "").is_ok());
    }

    #[test]
    fn wrong_checksum_is_rejected() {
        let error = verify_sha256(b"abc", "not-a-real-checksum").unwrap_err();
        assert_eq!(error, "Downloaded build failed checksum verification.");
    }
}
```

- [ ] **Step 2: Wire installer commands**

Modify `launcher/src-tauri/src/lib.rs`:

```rust
mod install_state;
mod installer;
mod manifest;

use install_state::InstallState;
use manifest::{current_platform, ReleaseManifest};
use tauri::Manager;

#[tauri::command]
fn read_install_state(app: tauri::AppHandle) -> Result<InstallState, String> {
    let app_data = app
        .path()
        .app_data_dir()
        .map_err(|error| format!("Could not resolve app data directory: {error}"))?;
    install_state::read_state(&app_data, current_platform())
}

#[tauri::command]
fn check_for_updates(manifest_url: String) -> Result<ReleaseManifest, String> {
    installer::fetch_manifest(&manifest_url)
}

#[tauri::command]
fn install_latest(
    app: tauri::AppHandle,
    manifest_url: String,
    force: bool,
) -> Result<InstallState, String> {
    let app_data = app
        .path()
        .app_data_dir()
        .map_err(|error| format!("Could not resolve app data directory: {error}"))?;
    let manifest = installer::fetch_manifest(&manifest_url)?;
    let release = manifest::platform_release(&manifest, current_platform())?;
    let archive_bytes = installer::download_archive(&release.url)?;
    installer::install_latest_from_manifest(&app_data, &manifest, &archive_bytes, force)
}

#[tauri::command]
fn launch_game(app: tauri::AppHandle) -> Result<(), String> {
    let app_data = app
        .path()
        .app_data_dir()
        .map_err(|error| format!("Could not resolve app data directory: {error}"))?;
    let state = install_state::read_state(&app_data, current_platform())?;
    if state.executable_path.is_empty() {
        return Err("No installed Trailblazers build was found. Use Repair / Reinstall first.".to_string());
    }
    crate::launcher::launch_installed_game(&state.executable_path)
}

mod launcher;

pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            read_install_state,
            check_for_updates,
            install_latest,
            launch_game
        ])
        .run(tauri::generate_context!())
        .expect("error while running Trailblazers Launcher");
}
```

- [ ] **Step 3: Run installer tests**

Run:

```bash
cd launcher/src-tauri
cargo test installer
```

Expected:

```text
test result: ok
```

- [ ] **Step 4: Commit installer flow**

Run:

```bash
git add launcher/src-tauri/src/installer.rs launcher/src-tauri/src/lib.rs
git commit -m "feat: install Trailblazers builds from release manifest"
```

## Play Button Launching

### Task 5: Launch Installed Ren'Py Builds on Windows and macOS

**Files:**
- Create: `launcher/src-tauri/src/launcher.rs`
- Modify: `launcher/src-tauri/src/lib.rs`

- [ ] **Step 1: Add launcher path tests and implementation**

Create `launcher/src-tauri/src/launcher.rs`:

```rust
use std::path::{Path, PathBuf};
use std::process::Command;

pub fn launch_target_for_install_path(path: &Path, platform: &str) -> Result<PathBuf, String> {
    if platform == "windows" {
        let direct = path.join("Trailblazers Trials.exe");
        if direct.exists() {
            return Ok(direct);
        }
        return find_extension(path, "exe")
            .ok_or_else(|| "No Windows executable was found in the installed build.".to_string());
    }

    if platform == "macos" {
        let direct = path.join("Trailblazers Trials.app");
        if direct.exists() {
            return Ok(direct);
        }
        return find_extension(path, "app")
            .ok_or_else(|| "No macOS app bundle was found in the installed build.".to_string());
    }

    Err("This launcher milestone supports Windows and macOS builds.".to_string())
}

fn find_extension(path: &Path, extension: &str) -> Option<PathBuf> {
    let entries = std::fs::read_dir(path).ok()?;
    for entry in entries.flatten() {
        let candidate = entry.path();
        if candidate
            .extension()
            .and_then(|value| value.to_str())
            .map(|value| value.eq_ignore_ascii_case(extension))
            .unwrap_or(false)
        {
            return Some(candidate);
        }
    }
    None
}

pub fn launch_installed_game(executable_path: &str) -> Result<(), String> {
    let install_path = PathBuf::from(executable_path);
    let platform = if cfg!(target_os = "windows") {
        "windows"
    } else if cfg!(target_os = "macos") {
        "macos"
    } else {
        "linux"
    };
    let target = launch_target_for_install_path(&install_path, platform)?;

    if platform == "macos" {
        Command::new("open")
            .arg(target)
            .spawn()
            .map_err(|error| format!("Could not launch macOS app: {error}"))?;
    } else {
        Command::new(target)
            .spawn()
            .map_err(|error| format!("Could not launch game executable: {error}"))?;
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn unsupported_platform_reports_scope() {
        let error = launch_target_for_install_path(Path::new("/tmp/game"), "linux").unwrap_err();
        assert_eq!(
            error,
            "This launcher milestone supports Windows and macOS builds."
        );
    }
}
```

- [ ] **Step 2: Run launcher tests**

Run:

```bash
cd launcher/src-tauri
cargo test launcher
```

Expected:

```text
test result: ok
```

- [ ] **Step 3: Run all launcher tests**

Run:

```bash
./launcher/scripts/test.sh
```

Expected:

```text
ok
test result: ok
```

- [ ] **Step 4: Commit play launching**

Run:

```bash
git add launcher/src-tauri/src/launcher.rs launcher/src-tauri/src/lib.rs
git commit -m "feat: launch installed Trailblazers builds"
```

## Release Workflow Documentation

### Task 6: Document Ren'Py Build and Launcher Release Process

**Files:**
- Create: `launcher/docs/release-workflow.md`
- Modify: `README.md`

- [ ] **Step 1: Add release workflow doc**

Create `launcher/docs/release-workflow.md`:

```markdown
# Trailblazers Launcher Release Workflow

## Build the Ren'Py Game

Open the Ren'Py SDK launcher from:

```text
/Users/murks/Web-Projects/renpy-8.5.2-sdk/renpy.app
```

Set the projects directory to:

```text
/Users/murks/Documents/Documents - murks’s MacBook Pro/Codex/2026-05-20-trailblazers-launcher-workspace
```

Select `trailblazers_trials`, then use the Ren'Py distribution screen to build
Windows and macOS packages.

## Name Release Assets

Use versioned names:

```text
Trailblazers-0.1.1-win.zip
Trailblazers-0.1.1-mac.zip
release-manifest.json
```

## Publish GitHub Release

Create a GitHub Release named `v0.1.1` and upload both game archives plus
`release-manifest.json`.

## Test Launcher Update

1. Open Trailblazers Launcher.
2. Click `Check for Updates`.
3. Confirm the latest version and patch notes appear.
4. Click `Repair / Reinstall`.
5. Confirm the correct platform build downloads and installs.
6. Click `Play`.
7. Confirm the packaged Ren'Py game opens.
```

- [ ] **Step 2: Add root README launcher section**

Append to `README.md`:

```markdown

## Trailblazers Launcher

The repository includes a launcher plan under `launcher/` for distributing
Windows and macOS builds without requiring players to install Ren'Py or clone
the repository.

The intended public distribution flow is:

1. Build the Ren'Py game through the Ren'Py SDK.
2. Upload versioned Windows/macOS archives to GitHub Releases.
3. Publish `release-manifest.json`.
4. Let testers install or update through Trailblazers Launcher.

See `launcher/docs/release-workflow.md` for the release checklist.
```

- [ ] **Step 3: Run docs check**

Run:

```bash
rg -n "Trailblazers Launcher|release-manifest.json|Repair / Reinstall" README.md launcher
```

Expected:

```text
README.md:...
launcher/docs/release-workflow.md:...
launcher/release-manifest.example.json:...
```

- [ ] **Step 4: Commit release docs**

Run:

```bash
git add README.md launcher/docs/release-workflow.md
git commit -m "docs: document launcher release workflow"
```

## Final Verification

### Task 7: Verify Launcher Milestone

**Files:**
- No new files.

- [ ] **Step 1: Run Ren'Py lint**

Run:

```bash
/Users/murks/Web-Projects/renpy-8.5.2-sdk/renpy.sh "/Users/murks/Documents/Documents - murks’s MacBook Pro/Codex/2026-05-20-trailblazers-launcher-workspace/trailblazers_trials" lint
```

Expected:

```text
Ren'Py 8.5.2...
The game contains ...
```

- [ ] **Step 2: Run Ren'Py tests**

Run:

```bash
python3 -m unittest discover -s trailblazers_trials/tests -v
```

Expected:

```text
Ran 26 tests
OK
```

- [ ] **Step 3: Run launcher tests**

Run:

```bash
./launcher/scripts/test.sh
```

Expected:

```text
ok
test result: ok
```

- [ ] **Step 4: Run Tauri development launcher**

Run:

```bash
./launcher/scripts/dev.sh
```

Expected:

```text
Trailblazers Launcher window opens.
```

Manual check:

- `Play` reports no installed build before repair/reinstall.
- `Check for Updates` reports a useful error if no public release manifest exists yet.
- `Repair / Reinstall` reports a useful error if no public release manifest exists yet.

- [ ] **Step 5: Commit verification adjustments**

If verification required small fixes, commit them:

```bash
git add launcher README.md .gitignore
git commit -m "fix: stabilize launcher milestone"
```

If no fixes were needed, do not create an empty commit.
