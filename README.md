# Trailblazers

This repository contains the current playable `Trailblazers Trials` prototype and related archive material.

## Repository Layout

- `trailblazers_trials/`
  - The active Ren'Py project.
  - Includes the game, assets, tests, and worldbuilding context files.
- `archive/tbtrlkk_prototype/`
  - An older prototype/starter project kept for reference only.

## Active Project

The main game lives in:

`trailblazers_trials`

Open that folder from the Ren'Py launcher to run the prototype.

## Current Chapter

- `Chapter 1: Heart of Fire`
- Location: `Anozira Village`

## Notes

- Generated saves, logs, caches, and compiled Ren'Py bytecode are excluded from version control.
- Worldbuilding canon and narrative context live under:
  - `trailblazers_trials/game/data/source_context/`

## Trailblazers Launcher

The launcher plan and implementation live under `launcher/`. The goal is to
distribute Windows and macOS builds of Trailblazers without asking testers to
install Ren'Py or clone this repository.

The intended release flow is: build the Ren'Py game, upload versioned Windows
and macOS archives to GitHub Releases, publish `release-manifest.json` beside
those archives, and let testers install or update through the launcher.

See `launcher/docs/release-workflow.md` for the Ren'Py build steps, GitHub
Release asset names, and launcher update test checklist.
