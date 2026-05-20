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
    fs::write(&path, contents).map_err(|error| format!("Could not write install state: {error}"))
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
