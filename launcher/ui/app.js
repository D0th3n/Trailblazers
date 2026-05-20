import {
  formatInstalledVersion,
  formatLatestVersion,
  isUpdateAvailable,
  platformLabel,
} from "./launcher-state.js";

export const DEFAULT_MANIFEST_URL =
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

function setButtonsDisabled(disabled) {
  elements.playButton.disabled = disabled;
  elements.checkButton.disabled = disabled;
  elements.repairButton.disabled = disabled;
}

function renderPatchNotes(notes) {
  elements.patchNotes.innerHTML = "";
  const releaseNotes = Array.isArray(notes) && notes.length ? notes : ["No release notes loaded."];

  for (const note of releaseNotes) {
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
  setButtonsDisabled(true);
  setStatus("Checking for updates...");

  try {
    latestManifest = await invoke("check_for_updates", {
      manifestUrl: DEFAULT_MANIFEST_URL,
    });
    render();
    if (isUpdateAvailable(installState?.installedVersion, latestManifest?.latestVersion)) {
      setStatus(`Update available: ${latestManifest.latestVersion}.`);
    } else {
      setStatus("Trailblazers is up to date.");
    }
  } catch (error) {
    setStatus(`Update check failed: ${error}`);
  } finally {
    setButtonsDisabled(false);
  }
}

async function repairOrReinstall() {
  setButtonsDisabled(true);
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
    setButtonsDisabled(false);
  }
}

async function playGame() {
  setButtonsDisabled(true);
  setStatus("Launching Trailblazers...");

  try {
    await invoke("launch_game");
    setStatus("Game launched.");
  } catch (error) {
    setStatus(`Launch failed: ${error}`);
  } finally {
    setButtonsDisabled(false);
  }
}

elements.checkButton.addEventListener("click", checkForUpdates);
elements.repairButton.addEventListener("click", repairOrReinstall);
elements.playButton.addEventListener("click", playGame);

render();
loadInstallState().catch((error) => {
  setStatus(`Could not read install state: ${error}`);
});
