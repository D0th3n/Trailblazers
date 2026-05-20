#!/bin/zsh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

cd "$REPO_ROOT"
node --test launcher/ui/launcher-state.test.mjs

if ! command -v cargo >/dev/null 2>&1; then
  echo "cargo not found; Rust tests skipped until the Tauri toolchain is installed."
elif [ ! -f "$REPO_ROOT/launcher/src-tauri/Cargo.toml" ]; then
  echo "launcher/src-tauri not found; Rust tests skipped until the Tauri backend is added."
else
  cd "$REPO_ROOT/launcher/src-tauri"
  cargo test
fi
