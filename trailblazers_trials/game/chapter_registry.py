CHAPTERS = [
    {
        "id": "chapter_01",
        "number": "Chapter 1",
        "roman": "Chapter I",
        "title": "Heart of Fire",
        "location": "Anozira Village",
        "summary": "Investigate the drought, trace the Moglim, and follow the heat beneath Anozira.",
        "tagline": "Acerima's drought is only the beginning.",
        "menu_background": "bg village square",
        "start_label": "chapter_01",
        "available": True,
        "checkpoints": [
            {
                "label": "chapter_01",
                "menu_label": "Opening",
                "description": "Begin Heart of Fire from the opening recap.",
            },
            {
                "label": "chapter_01_checkpoint_evening",
                "menu_label": "Evening Interlude",
                "description": "Skip to the village night scenes and Ruzen setup.",
            },
            {
                "label": "chapter_01_checkpoint_mine",
                "menu_label": "Ruzen Mine Approach",
                "description": "Jump to the mine lead-in and Titan route.",
            },
        ],
    },
]


def featured_chapter():
    for chapter in CHAPTERS:
        if chapter.get("available", False):
            return chapter
    return CHAPTERS[0]


def chapter_card_entries():
    return [chapter for chapter in CHAPTERS if chapter.get("available", False)]


def checkpoint_entries():
    entries = []
    for chapter in chapter_card_entries():
        for checkpoint in chapter.get("checkpoints", []):
            entry = dict(checkpoint)
            entry["chapter_id"] = chapter["id"]
            entry["chapter_number"] = chapter["number"]
            entry["chapter_title"] = chapter["title"]
            entries.append(entry)
    return entries


def playable_label_set():
    labels = set()
    for chapter in chapter_card_entries():
        labels.add(chapter["start_label"])
        for checkpoint in chapter.get("checkpoints", []):
            labels.add(checkpoint["label"])
    return labels

