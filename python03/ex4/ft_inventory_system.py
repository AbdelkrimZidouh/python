import sys


def parse_inventory(args: list) -> dict:
    inventory = dict()
    for param in args:
        if ':' not in param or param.count(':') != 1:
            print(f"Error - invalid parameter '{param}'")
            continue
        name, quantity = param.split(':')
        if name in inventory:
            print(f"Redundant item '{name}' - discarding")
            continue
        try:
            inventory.update({name: int(quantity)})
        except ValueError as e:
            print(f"Quantity error for '{name}': {e}")
    return inventory


def display_analysis(inventory: dict) -> None:
    print(f"Got inventory: {inventory}")

    item_list = list(inventory.keys())
    print(f"Item list: {item_list}")

    if not item_list:
        print("No items to analyze.")
        return

    total = sum(inventory.values())
    print(f"Total quantity of the {len(item_list)} items: {total}")

    for item in item_list:
        pct = round(inventory[item] / total * 100, 1)
        print(f"Item {item} represents {pct}%")

    most = item_list[0]
    least = item_list[0]
    for item in item_list:
        if inventory[item] > inventory[most]:
            most = item
        if inventory[item] < inventory[least]:
            least = item

    print(f"Item most abundant: {most} with quantity {inventory[most]}")
    print(f"Item least abundant: {least} with quantity {inventory[least]}")


def main() -> None:
    print("=== Inventory System Analysis ===")
    inventory = parse_inventory(sys.argv[1:])
    display_analysis(inventory)
    inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
