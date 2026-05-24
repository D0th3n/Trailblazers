import {
  formatInstalledVersion,
  formatLatestVersion,
  isUpdateAvailable,
  normalizeNewsItems,
  platformLabel,
} from "./launcher-state.js";

export const DEFAULT_MANIFEST_URL =
  "https://github.com/D0th3n/Trailblazers/releases/latest/download/release-manifest.json";

const tauriInvoke = window.__TAURI__?.core?.invoke;
const DEFAULT_NEWS_FEED = {
  news: [
    {
      title: "Quality of life update out now!",
      body: "Launcher and early gameplay polish are being refreshed as Trailblazers Trials grows.",
    },
  ],
  lore: [
    {
      title: "Lore updates coming soon",
      body: "Future notes will preview qana, races, locations, and chapter context.",
    },
  ],
  media: [
    {
      title: "Media updates coming soon",
      body: "Art, music, screenshots, and other creation updates will appear here.",
    },
  ],
};

const elements = {
  platformLabel: document.querySelector("#platformLabel"),
  installedVersion: document.querySelector("#installedVersion"),
  latestVersion: document.querySelector("#latestVersion"),
  playButton: document.querySelector("#playButton"),
  checkButton: document.querySelector("#checkButton"),
  repairButton: document.querySelector("#repairButton"),
  statusText: document.querySelector("#statusText"),
  newsItems: document.querySelector("#newsItems"),
  newsTabs: document.querySelectorAll("[data-news-tab]"),
};

let installState = null;
let latestManifest = null;
let newsFeed = DEFAULT_NEWS_FEED;
let activeNewsTab = "news";

function setStatus(message) {
  elements.statusText.textContent = message;
}

function setButtonsDisabled(disabled) {
  elements.playButton.disabled = disabled;
  elements.checkButton.disabled = disabled;
  elements.repairButton.disabled = disabled;
}

function patchNotesFeedItems(notes) {
  const releaseNotes =
    Array.isArray(notes) && notes.length
      ? notes
      : ["Check for updates to load the latest release notes."];

  return releaseNotes.map((note) => ({
    title: "",
    body: note,
  }));
}

function currentNewsItems() {
  if (activeNewsTab === "patch") {
    return patchNotesFeedItems(latestManifest?.releaseNotes);
  }

  const items = normalizeNewsItems(newsFeed, activeNewsTab);
  if (items.length) {
    return items;
  }

  return [
    {
      title: "More updates coming soon",
      body: "New launcher posts will appear here as Trailblazers Trials expands.",
    },
  ];
}

function renderNewsItems() {
  elements.newsItems.innerHTML = "";

  for (const newsItem of currentNewsItems()) {
    const item = document.createElement("li");
    if (newsItem.title) {
      const title = document.createElement("strong");
      title.textContent = newsItem.title;
      item.append(title);
    }
    if (newsItem.body) {
      const body = document.createElement("span");
      body.textContent = newsItem.body;
      item.append(body);
    }
    elements.newsItems.append(item);
  }
}

function renderNewsTabs() {
  for (const tab of elements.newsTabs) {
    const selected = tab.dataset.newsTab === activeNewsTab;
    tab.classList.toggle("is-active", selected);
    tab.setAttribute("aria-pressed", String(selected));
  }
}

function render() {
  elements.platformLabel.textContent = `Platform: ${platformLabel(installState?.platform)}`;
  elements.installedVersion.textContent = formatInstalledVersion(installState);
  elements.latestVersion.textContent = formatLatestVersion(latestManifest);
  renderNewsTabs();
  renderNewsItems();
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

async function loadNewsFeed() {
  try {
    const response = await fetch("./news-feed.json", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    newsFeed = await response.json();
  } catch (error) {
    newsFeed = DEFAULT_NEWS_FEED;
  }
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
for (const tab of elements.newsTabs) {
  tab.addEventListener("click", () => {
    activeNewsTab = tab.dataset.newsTab;
    render();
  });
}

render();
loadNewsFeed();
loadInstallState().catch((error) => {
  setStatus(`Could not read install state: ${error}`);
});
