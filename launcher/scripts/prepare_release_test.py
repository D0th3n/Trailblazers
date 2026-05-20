#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("prepare_release.py")


def load_prepare_release():
    spec = importlib.util.spec_from_file_location("prepare_release", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PrepareReleaseTest(unittest.TestCase):
    def setUp(self):
        self.prepare_release = load_prepare_release()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.windows_archive = self.root / "Trailblazers-0.1.1-win.zip"
        self.macos_archive = self.root / "Trailblazers-0.1.1-mac.zip"
        self.windows_archive.write_bytes(b"windows-build")
        self.macos_archive.write_bytes(b"macos-build")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_sha256_file_hashes_archive_bytes(self):
        expected = hashlib.sha256(b"windows-build").hexdigest()

        actual = self.prepare_release.sha256_file(self.windows_archive)

        self.assertEqual(actual, expected)

    def test_build_manifest_matches_launcher_contract(self):
        manifest = self.prepare_release.build_manifest(
            version="0.1.1",
            windows_archive=self.windows_archive,
            macos_archive=self.macos_archive,
            notes=[
                "Expanded Chapter 1 investigation flow.",
                "Added updated Anozira assets.",
            ],
            repo="D0th3n/Trailblazers",
            game_id="trailblazers-trials",
            minimum_launcher_version="0.1.0",
        )

        self.assertEqual(manifest["gameId"], "trailblazers-trials")
        self.assertEqual(manifest["latestVersion"], "0.1.1")
        self.assertEqual(
            manifest["releaseNotes"],
            [
                "Expanded Chapter 1 investigation flow.",
                "Added updated Anozira assets.",
            ],
        )
        self.assertEqual(manifest["minimumLauncherVersion"], "0.1.0")
        self.assertEqual(
            manifest["platforms"]["windows"],
            {
                "archive": "Trailblazers-0.1.1-win.zip",
                "url": "https://github.com/D0th3n/Trailblazers/releases/download/v0.1.1/Trailblazers-0.1.1-win.zip",
                "sha256": hashlib.sha256(b"windows-build").hexdigest(),
            },
        )
        self.assertEqual(
            manifest["platforms"]["macos"],
            {
                "archive": "Trailblazers-0.1.1-mac.zip",
                "url": "https://github.com/D0th3n/Trailblazers/releases/download/v0.1.1/Trailblazers-0.1.1-mac.zip",
                "sha256": hashlib.sha256(b"macos-build").hexdigest(),
            },
        )

    def test_cli_writes_manifest_json(self):
        output_path = self.root / "release-manifest.json"

        subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--version",
                "0.1.1",
                "--windows-archive",
                str(self.windows_archive),
                "--macos-archive",
                str(self.macos_archive),
                "--note",
                "Expanded Chapter 1 investigation flow.",
                "--note",
                "Added updated Anozira assets.",
                "--output",
                str(output_path),
            ],
            check=True,
        )

        manifest = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["latestVersion"], "0.1.1")
        self.assertEqual(
            manifest["platforms"]["windows"]["sha256"],
            hashlib.sha256(b"windows-build").hexdigest(),
        )
        self.assertTrue(output_path.read_text(encoding="utf-8").endswith("\n"))


if __name__ == "__main__":
    unittest.main()
