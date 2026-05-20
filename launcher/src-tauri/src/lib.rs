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
    let installed = install_state::read_state(&app_data, current_platform())?;
    if !installer::update_is_needed(&installed, &manifest, force) {
        return Ok(installed);
    }

    let release = manifest::platform_release(&manifest, current_platform())?;
    let archive_bytes = installer::download_archive(&release.url)?;
    installer::install_latest_from_manifest(&app_data, &manifest, &archive_bytes, force)
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
