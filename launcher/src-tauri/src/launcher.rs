use crate::manifest;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;

pub fn launch_target_for_install_path(path: &Path, platform: &str) -> Result<PathBuf, String> {
    let install_path = install_path_for(path, platform);

    match platform {
        "windows" => windows_launch_target(&install_path),
        "macos" => macos_launch_target(&install_path),
        _ => Err("This launcher milestone supports Windows and macOS builds.".to_string()),
    }
}

pub fn launch_installed_game(executable_path: &str) -> Result<(), String> {
    let platform = manifest::current_platform();
    let target = launch_target_for_install_path(Path::new(executable_path), platform)?;

    let mut command = match platform {
        "macos" => {
            let mut command = Command::new("open");
            command.arg(&target);
            command
        }
        "windows" => Command::new(&target),
        _ => return Err("This launcher milestone supports Windows and macOS builds.".to_string()),
    };

    command
        .spawn()
        .map_err(|error| format!("Could not launch Trailblazers: {error}"))?;
    Ok(())
}

fn install_path_for(path: &Path, platform: &str) -> PathBuf {
    let platform_extension = match platform {
        "windows" => "exe",
        "macos" => "app",
        _ => return path.to_path_buf(),
    };

    if path.exists() {
        if has_extension(path, platform_extension) {
            return path.to_path_buf();
        }
        return path.to_path_buf();
    }

    if has_extension(path, platform_extension) {
        if let Some(parent) = path.parent() {
            return parent.to_path_buf();
        }
    }

    path.to_path_buf()
}

fn windows_launch_target(install_path: &Path) -> Result<PathBuf, String> {
    if install_path.is_file() && has_extension(install_path, "exe") {
        return Ok(install_path.to_path_buf());
    }

    let preferred = install_path.join("Trailblazers Trials.exe");
    if preferred.is_file() {
        return Ok(preferred);
    }

    find_child_with_extension(install_path, "exe", |path| path.is_file())
        .ok_or_else(|| "No Windows executable was found in the installed build.".to_string())
}

fn macos_launch_target(install_path: &Path) -> Result<PathBuf, String> {
    if install_path.is_dir() && has_extension(install_path, "app") {
        return Ok(install_path.to_path_buf());
    }

    let preferred = install_path.join("Trailblazers Trials.app");
    if preferred.is_dir() {
        return Ok(preferred);
    }

    find_child_with_extension(install_path, "app", |path| path.is_dir())
        .ok_or_else(|| "No macOS app bundle was found in the installed build.".to_string())
}

fn find_child_with_extension<F>(path: &Path, extension: &str, predicate: F) -> Option<PathBuf>
where
    F: Fn(&Path) -> bool,
{
    let mut candidates = fs::read_dir(path)
        .ok()?
        .filter_map(|entry| entry.ok().map(|entry| entry.path()))
        .filter(|path| has_extension(path, extension) && predicate(path))
        .collect::<Vec<_>>();
    candidates.sort();
    candidates.into_iter().next()
}

fn has_extension(path: &Path, expected: &str) -> bool {
    path.extension()
        .and_then(|extension| extension.to_str())
        .is_some_and(|extension| extension.eq_ignore_ascii_case(expected))
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    #[test]
    fn unsupported_platform_reports_milestone_scope() {
        let temp_dir = tempfile::tempdir().unwrap();
        let error = launch_target_for_install_path(temp_dir.path(), "linux").unwrap_err();
        assert_eq!(
            error,
            "This launcher milestone supports Windows and macOS builds."
        );
    }

    #[test]
    fn windows_prefers_direct_trailblazers_trials_exe() {
        let temp_dir = tempfile::tempdir().unwrap();
        fs::write(temp_dir.path().join("Other.exe"), "").unwrap();
        fs::write(temp_dir.path().join("Trailblazers Trials.exe"), "").unwrap();

        let target = launch_target_for_install_path(temp_dir.path(), "windows").unwrap();
        assert_eq!(target, temp_dir.path().join("Trailblazers Trials.exe"));
    }

    #[test]
    fn windows_falls_back_to_any_exe() {
        let temp_dir = tempfile::tempdir().unwrap();
        fs::write(temp_dir.path().join("RenpyBuild.exe"), "").unwrap();

        let target = launch_target_for_install_path(temp_dir.path(), "windows").unwrap();
        assert_eq!(target, temp_dir.path().join("RenpyBuild.exe"));
    }

    #[test]
    fn windows_reports_missing_executable() {
        let temp_dir = tempfile::tempdir().unwrap();
        let error = launch_target_for_install_path(temp_dir.path(), "windows").unwrap_err();
        assert_eq!(
            error,
            "No Windows executable was found in the installed build."
        );
    }

    #[test]
    fn macos_prefers_direct_trailblazers_trials_app() {
        let temp_dir = tempfile::tempdir().unwrap();
        fs::create_dir(temp_dir.path().join("Other.app")).unwrap();
        fs::create_dir(temp_dir.path().join("Trailblazers Trials.app")).unwrap();

        let target = launch_target_for_install_path(temp_dir.path(), "macos").unwrap();
        assert_eq!(target, temp_dir.path().join("Trailblazers Trials.app"));
    }

    #[test]
    fn macos_falls_back_to_any_app() {
        let temp_dir = tempfile::tempdir().unwrap();
        fs::create_dir(temp_dir.path().join("RenpyBuild.app")).unwrap();

        let target = launch_target_for_install_path(temp_dir.path(), "macos").unwrap();
        assert_eq!(target, temp_dir.path().join("RenpyBuild.app"));
    }

    #[test]
    fn macos_reports_missing_app_bundle() {
        let temp_dir = tempfile::tempdir().unwrap();
        let error = launch_target_for_install_path(temp_dir.path(), "macos").unwrap_err();
        assert_eq!(
            error,
            "No macOS app bundle was found in the installed build."
        );
    }
}
