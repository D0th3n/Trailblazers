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
