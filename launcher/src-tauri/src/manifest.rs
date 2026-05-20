use serde::{Deserialize, Serialize};
use std::cmp::Ordering;
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

pub fn compare_versions(left: &str, right: &str) -> Ordering {
    let left_parts = version_parts(left);
    let right_parts = version_parts(right);
    let length = left_parts.len().max(right_parts.len());

    for index in 0..length {
        let left_part = *left_parts.get(index).unwrap_or(&0);
        let right_part = *right_parts.get(index).unwrap_or(&0);
        match left_part.cmp(&right_part) {
            Ordering::Equal => {}
            ordering => return ordering,
        }
    }

    Ordering::Equal
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
        let manifest = manifest();
        let release = platform_release(&manifest, "windows").unwrap();
        assert_eq!(release.archive, "Trailblazers-0.1.1-win.zip");
    }

    #[test]
    fn platform_release_reports_missing_build() {
        let error = platform_release(&manifest(), "macos").unwrap_err();
        assert_eq!(error, "No Trailblazers build is available for macos.");
    }

    #[test]
    fn orders_dotted_versions_numerically() {
        assert_eq!(compare_versions("0.1.10", "0.1.9"), Ordering::Greater);
        assert_eq!(compare_versions("0.1.9", "0.1.10"), Ordering::Less);
        assert_eq!(compare_versions("1.0.0", "1.0"), Ordering::Equal);
    }
}
