init python:
    import sys

    game_python_root = config.gamedir
    if game_python_root not in sys.path:
        sys.path.insert(0, game_python_root)

    import inventory
    import store

    def tb_inventory_add(item_id, quantity=1):
        store.tb_inventory = inventory.add_item(
            store.tb_inventory,
            item_id,
            quantity,
        )

    def tb_inventory_take_room_supplies():
        tb_inventory_add("health_elixir", 1)
        tb_inventory_add("qana_elixir", 1)

    def tb_inventory_count(item_id):
        return inventory.item_count(store.tb_inventory, item_id)

    def tb_inventory_summary():
        return inventory.inventory_summary(store.tb_inventory)
