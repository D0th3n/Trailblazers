import test from "node:test";
import assert from "node:assert/strict";
import {
  formatInstalledVersion,
  formatLatestVersion,
  isUpdateAvailable,
  normalizeNewsItems,
  platformLabel,
  versionParts,
} from "./launcher-state.js";

test("formatInstalledVersion describes missing installs", () => {
  assert.equal(formatInstalledVersion(null), "Not installed");
  assert.equal(formatInstalledVersion({ installedVersion: "" }), "Not installed");
  assert.equal(formatInstalledVersion({ installedVersion: "   " }), "Not installed");
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

test("versionParts parses semantic numeric version segments", () => {
  assert.deepEqual(versionParts("0.1.10"), [0, 1, 10]);
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

test("normalizeNewsItems returns clean title and body pairs for a category", () => {
  assert.deepEqual(
    normalizeNewsItems(
      {
        news: [
          { title: " Quality of life update out now! ", body: " Launcher polish. " },
          { title: "", body: "" },
          null,
        ],
      },
      "news",
    ),
    [{ title: "Quality of life update out now!", body: "Launcher polish." }],
  );
  assert.deepEqual(normalizeNewsItems({}, "media"), []);
});
