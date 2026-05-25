ITEM_DEFINITIONS = {
    "health_elixir": {
        "label": "Health Elixir",
        "description": "Restores a small amount of HP in battle.",
    },
    "qana_elixir": {
        "label": "Qana Elixir",
        "description": "Restores a small amount of Qana in battle.",
    },
}


def normalized_inventory(inventory):
    return dict(inventory or {})


def add_item(inventory, item_id, quantity=1):
    updated = normalized_inventory(inventory)
    updated[item_id] = max(0, updated.get(item_id, 0) + quantity)
    return updated


def item_count(inventory, item_id):
    return normalized_inventory(inventory).get(item_id, 0)


def inventory_summary(inventory):
    counts = normalized_inventory(inventory)
    entries = []

    for item_id, data in ITEM_DEFINITIONS.items():
        count = counts.get(item_id, 0)
        if count:
            entries.append("%s x%d" % (data["label"], count))

    if not entries:
        return "Inventory: Empty"

    return "Inventory: " + " | ".join(entries)
