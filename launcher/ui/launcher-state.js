export function formatInstalledVersion(state) {
  const installedVersion = state?.installedVersion?.trim();
  if (!installedVersion) {
    return "Not installed";
  }

  return `Installed: ${installedVersion}`;
}

export function formatLatestVersion(manifest) {
  const latestVersion = manifest?.latestVersion?.trim();
  if (!latestVersion) {
    return "Latest: not checked";
  }

  return `Latest: ${latestVersion}`;
}

export function versionParts(version) {
  return String(version ?? "")
    .split(".")
    .map((part) => Number.parseInt(part, 10))
    .map((part) => (Number.isFinite(part) ? part : 0));
}

export function isUpdateAvailable(installedVersion, latestVersion) {
  const installed = versionParts(installedVersion);
  const latest = versionParts(latestVersion);
  const length = Math.max(installed.length, latest.length);

  for (let index = 0; index < length; index += 1) {
    const installedPart = installed[index] ?? 0;
    const latestPart = latest[index] ?? 0;

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
