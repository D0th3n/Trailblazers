use crate::install_state::{self, InstallState};
use crate::manifest::{self, ReleaseManifest};
use sha2::{Digest, Sha256};
use std::cmp::Ordering;
use std::fs;
use std::io::Cursor;
use std::path::{Component, Path, PathBuf};
use zip::ZipArchive;

pub fn update_is_needed(installed: &InstallState, manifest: &ReleaseManifest, force: bool) -> bool {
    force
        || installed.installed_version.is_empty()
        || manifest::compare_versions(&manifest.latest_version, &installed.installed_version)
            == Ordering::Greater
}

pub fn verify_sha256(bytes: &[u8], expected: &str) -> Result<(), String> {
    let expected = expected.trim();
    if expected.is_empty() {
        return Ok(());
    }

    let actual = format!("{:x}", Sha256::digest(bytes));
    if actual.eq_ignore_ascii_case(expected) {
        Ok(())
    } else {
        Err("Downloaded build failed checksum verification.".to_string())
    }
}

pub fn extract_zip(bytes: &[u8], destination: &Path) -> Result<(), String> {
    fs::create_dir_all(destination)
        .map_err(|error| format!("Could not create install extraction folder: {error}"))?;

    let cursor = Cursor::new(bytes);
    let mut archive = ZipArchive::new(cursor)
        .map_err(|error| format!("Could not read downloaded build archive: {error}"))?;

    for index in 0..archive.len() {
        let mut file = archive
            .by_index(index)
            .map_err(|error| format!("Could not read downloaded build archive entry: {error}"))?;
        let enclosed_name = safe_zip_path(file.name())?;
        let output_path = destination.join(enclosed_name);

        if file.is_dir() {
            fs::create_dir_all(&output_path)
                .map_err(|error| format!("Could not create install folder: {error}"))?;
            continue;
        }

        if let Some(parent) = output_path.parent() {
            fs::create_dir_all(parent)
                .map_err(|error| format!("Could not create install folder: {error}"))?;
        }

        let mut output = fs::File::create(&output_path)
            .map_err(|error| format!("Could not extract build file: {error}"))?;
        std::io::copy(&mut file, &mut output)
            .map_err(|error| format!("Could not write build file: {error}"))?;
    }

    Ok(())
}

pub fn fetch_manifest(manifest_url: &str) -> Result<ReleaseManifest, String> {
    reqwest::blocking::get(manifest_url)
        .map_err(|error| format!("Could not fetch release manifest: {error}"))?
        .error_for_status()
        .map_err(|error| format!("Could not fetch release manifest: {error}"))?
        .json::<ReleaseManifest>()
        .map_err(|error| format!("Could not parse release manifest: {error}"))
}

pub fn download_archive(url: &str) -> Result<Vec<u8>, String> {
    let response = reqwest::blocking::get(url)
        .map_err(|error| format!("Could not download Trailblazers build: {error}"))?
        .error_for_status()
        .map_err(|error| format!("Could not download Trailblazers build: {error}"))?;
    response
        .bytes()
        .map(|bytes| bytes.to_vec())
        .map_err(|error| format!("Could not read Trailblazers build download: {error}"))
}

pub fn install_latest_from_manifest(
    app_data_dir: &Path,
    manifest: &ReleaseManifest,
    archive_bytes: &[u8],
    force: bool,
) -> Result<InstallState, String> {
    let platform = manifest::current_platform();
    let release = manifest::platform_release(manifest, platform)?;
    let installed = install_state::read_state(app_data_dir, platform)?;

    if !update_is_needed(&installed, manifest, force) {
        return Ok(installed);
    }

    verify_sha256(archive_bytes, &release.sha256)?;

    let current_dir = install_state::current_game_dir(app_data_dir);
    let parent_dir = current_dir
        .parent()
        .ok_or_else(|| "Could not resolve install folder.".to_string())?;
    fs::create_dir_all(parent_dir)
        .map_err(|error| format!("Could not create install folder: {error}"))?;

    let temp_dir = tempfile::tempdir_in(parent_dir)
        .map_err(|error| format!("Could not create temporary install folder: {error}"))?;
    extract_zip(archive_bytes, temp_dir.path())?;

    if current_dir.exists() {
        fs::remove_dir_all(&current_dir)
            .map_err(|error| format!("Could not replace installed build: {error}"))?;
    }
    fs::rename(temp_dir.path(), &current_dir)
        .map_err(|error| format!("Could not move build into install folder: {error}"))?;

    let state = InstallState {
        installed_version: manifest.latest_version.clone(),
        platform: platform.to_string(),
        installed_at: install_state::now_iso(),
        last_manual_update_check_at: installed.last_manual_update_check_at,
        executable_path: executable_path(&current_dir, platform),
    };
    install_state::write_state(app_data_dir, &state)?;

    Ok(state)
}

fn safe_zip_path(name: &str) -> Result<PathBuf, String> {
    let path = Path::new(name);
    if path.components().any(|component| {
        matches!(
            component,
            Component::ParentDir | Component::RootDir | Component::Prefix(_)
        )
    }) {
        return Err(format!(
            "Downloaded build archive contains unsafe path: {name}"
        ));
    }

    Ok(path.to_path_buf())
}

fn executable_path(current_dir: &Path, platform: &str) -> String {
    match platform {
        "windows" => current_dir.join("Trailblazers.exe"),
        "macos" => current_dir.join("Trailblazers.app"),
        _ => current_dir.join("Trailblazers.sh"),
    }
    .to_string_lossy()
    .to_string()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::install_state::InstallState;
    use crate::manifest::{PlatformRelease, ReleaseManifest};
    use std::collections::BTreeMap;
    use std::io::{Cursor, Write};
    use zip::write::SimpleFileOptions;

    fn manifest(version: &str) -> ReleaseManifest {
        let mut platforms = BTreeMap::new();
        platforms.insert(
            "macos".to_string(),
            PlatformRelease {
                archive: format!("Trailblazers-{version}-mac.zip"),
                url: "https://example.test/mac.zip".to_string(),
                sha256: String::new(),
            },
        );

        ReleaseManifest {
            game_id: "trailblazers-trials".to_string(),
            latest_version: version.to_string(),
            release_notes: vec![],
            minimum_launcher_version: "0.1.0".to_string(),
            platforms,
        }
    }

    fn installed(version: &str) -> InstallState {
        InstallState {
            installed_version: version.to_string(),
            platform: "macos".to_string(),
            installed_at: "2026-05-20T00:00:00Z".to_string(),
            last_manual_update_check_at: None,
            executable_path: "/tmp/Trailblazers".to_string(),
        }
    }

    #[test]
    fn update_is_needed_when_forced_missing_or_manifest_is_newer() {
        assert!(update_is_needed(
            &installed("0.1.1"),
            &manifest("0.1.1"),
            true
        ));
        assert!(update_is_needed(
            &InstallState::empty("macos"),
            &manifest("0.1.1"),
            false
        ));
        assert!(update_is_needed(
            &installed("0.1.0"),
            &manifest("0.1.1"),
            false
        ));
    }

    #[test]
    fn update_is_not_needed_when_installed_version_matches_manifest() {
        assert!(!update_is_needed(
            &installed("0.1.1"),
            &manifest("0.1.1"),
            false
        ));
    }

    #[test]
    fn verify_sha256_accepts_blank_expected_checksum() {
        verify_sha256(b"downloaded bytes", "").unwrap();
    }

    #[test]
    fn verify_sha256_rejects_wrong_checksum_with_expected_error() {
        let error = verify_sha256(b"downloaded bytes", "not-the-right-checksum").unwrap_err();
        assert_eq!(error, "Downloaded build failed checksum verification.");
    }

    #[test]
    fn extract_zip_rejects_unsafe_parent_paths() {
        let mut archive_bytes = Cursor::new(Vec::new());
        {
            let mut zip = zip::ZipWriter::new(&mut archive_bytes);
            zip.start_file("../escape.txt", SimpleFileOptions::default())
                .unwrap();
            zip.write_all(b"bad").unwrap();
            zip.finish().unwrap();
        }

        let temp_dir = tempfile::tempdir().unwrap();
        let error = extract_zip(archive_bytes.get_ref(), temp_dir.path()).unwrap_err();
        assert!(error.contains("unsafe path"));
    }
}
