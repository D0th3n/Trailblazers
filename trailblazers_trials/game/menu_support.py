from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path


WORLD_HISTORY_OVERVIEW = (
    "Before Anozira's wells began to steam dry, the world of Trailblazers had already survived a greater age of ruin. "
    "Long ago, dragons ruled openly, with Drysk serving as their noble intermediaries while humanity and the other lower races lived beneath their order. "
    "That age broke when Jyra, daughter of the Highest Order, led the human revolt with Arthur, the dragon of healing light, at her side.\n\n"
    "The revolt sealed the dragons away and founded Acerima, but it did not make the world simple. "
    "The blood of Jyra and Arthur still shapes the royal line, the Highest Order still shadows mortal belief, and hidden forces like Severence still search for ways to bend reality back toward their own design.\n\n"
    "In the age that followed, civilization learned to live with Qana instead of treating it as myth. "
    "Qana is the field beneath matter, weather, creatures, memory, and spells. Human kingdoms regulate it, schools study it, hunters survive by understanding it, and Qana recyclers carve out safe settlements from lands that would otherwise belong to monsters.\n\n"
    "Now the old history presses against the present again. "
    "Dragons are believed sealed, Qana storms still warp the wilds, and every village crisis risks being tied to something larger beneath the surface. "
    "Trailblazers Trials begins in that pressure point: a small drought in Anozira, a kingdom slow to respond, and one young squire already living beside truths the world has forgotten."
)


def issue_report_directory(game_dir: str | Path) -> Path:
    return Path(game_dir) / "player_reports"


def submit_issue_report(
    game_dir: str | Path,
    subject: str,
    details: str,
    *,
    player_name: str = "",
) -> str:
    report_dir = issue_report_directory(game_dir)
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / "issue_reports.jsonl"
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "player_name": player_name.strip(),
        "subject": subject.strip(),
        "details": details.strip(),
    }

    with report_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=True) + "\n")

    return str(report_path)
