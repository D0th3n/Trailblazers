#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path


DEFAULT_REPO = "D0th3n/Trailblazers"
DEFAULT_GAME_ID = "trailblazers-trials"
DEFAULT_MINIMUM_LAUNCHER_VERSION = "0.1.0"


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as archive:
        for chunk in iter(lambda: archive.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def release_tag(version):
    return version if version.startswith("v") else f"v{version}"


def release_asset_url(repo, version, archive):
    return (
        f"https://github.com/{repo}/releases/download/"
        f"{release_tag(version)}/{archive.name}"
    )


def platform_manifest(repo, version, archive):
    return {
        "archive": archive.name,
        "url": release_asset_url(repo, version, archive),
        "sha256": sha256_file(archive),
    }


def build_manifest(
    *,
    version,
    windows_archive,
    macos_archive,
    notes,
    repo=DEFAULT_REPO,
    game_id=DEFAULT_GAME_ID,
    minimum_launcher_version=DEFAULT_MINIMUM_LAUNCHER_VERSION,
):
    return {
        "gameId": game_id,
        "latestVersion": version,
        "releaseNotes": notes,
        "minimumLauncherVersion": minimum_launcher_version,
        "platforms": {
            "windows": platform_manifest(repo, version, windows_archive),
            "macos": platform_manifest(repo, version, macos_archive),
        },
    }


def notes_from_file(path):
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def collect_notes(args):
    notes = list(args.note or [])
    if args.notes_file:
        notes.extend(notes_from_file(args.notes_file))
    if not notes:
        raise SystemExit("Add at least one release note with --note or --notes-file.")
    return notes


def existing_file(value):
    path = Path(value)
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"{path} is not a file")
    return path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create the Trailblazers launcher release-manifest.json."
    )
    parser.add_argument("--version", required=True, help="Game version, e.g. 0.1.1")
    parser.add_argument(
        "--windows-archive",
        required=True,
        type=existing_file,
        help="Path to the Windows Ren'Py zip archive",
    )
    parser.add_argument(
        "--macos-archive",
        required=True,
        type=existing_file,
        help="Path to the macOS Ren'Py zip archive",
    )
    parser.add_argument(
        "--note",
        action="append",
        help="Release note line. Repeat for multiple notes.",
    )
    parser.add_argument(
        "--notes-file",
        type=existing_file,
        help="Optional UTF-8 text file with one release note per line.",
    )
    parser.add_argument(
        "--output",
        default="release-manifest.json",
        type=Path,
        help="Manifest output path",
    )
    parser.add_argument(
        "--repo",
        default=DEFAULT_REPO,
        help="GitHub owner/repo used for release asset URLs",
    )
    parser.add_argument(
        "--game-id",
        default=DEFAULT_GAME_ID,
        help="Game id expected by the launcher",
    )
    parser.add_argument(
        "--minimum-launcher-version",
        default=DEFAULT_MINIMUM_LAUNCHER_VERSION,
        help="Oldest launcher version allowed to install this game release",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    manifest = build_manifest(
        version=args.version,
        windows_archive=args.windows_archive,
        macos_archive=args.macos_archive,
        notes=collect_notes(args),
        repo=args.repo,
        game_id=args.game_id,
        minimum_launcher_version=args.minimum_launcher_version,
    )
    args.output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
