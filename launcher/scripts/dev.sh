#!/bin/zsh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

if ! command -v cargo >/dev/null 2>&1; then
  echo "cargo not found. Install Rust with rustup before running the launcher."
  exit 1
fi

cd "$REPO_ROOT/launcher/src-tauri"
cargo tauri dev
