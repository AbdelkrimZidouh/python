from collections.abc import Callable
from typing import Any


def mage_counter() -> Callable[[], int]:
    invocations = 0

    def tally() -> int:
        nonlocal invocations
        invocations += 1
        return invocations

    return tally


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    running_total = initial_power

    def charge(amount: int) -> int:
        nonlocal running_total
        running_total += amount
        return running_total

    return charge


def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:
    def enchant_item(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"

    return enchant_item


def memory_vault() -> dict[str, Callable]:
    _db: dict[str, Any] = {}

    def put_data(key: str, value: Any) -> None:
        _db[key] = value

    def get_data(key: str) -> Any:
        if key in _db:
            return _db[key]
        return "Memory not found"

    return {"store": put_data, "recall": get_data}


def main() -> None:
    print("Testing mage counter...")
    ca = mage_counter()
    cb = mage_counter()
    print(f"counter_a call 1: {ca()}")
    print(f"counter_a call 2: {ca()}")
    print(f"counter_b call 1: {cb()}")

    print("\nTesting spell accumulator...")
    acc = spell_accumulator(100)
    print(f"Base 100, add 20: {acc(20)}")
    print(f"Base 100, add 30: {acc(30)}")

    print("\nTesting enchantment factory...")
    fire = enchantment_factory("Flaming")
    ice = enchantment_factory("Frozen")
    print(fire("Sword"))
    print(ice("Shield"))

    print("\nTesting memory vault...")
    v = memory_vault()
    print("Store 'secret' = 42")
    v["store"]("secret", 42)
    print(f"Recall 'secret': {v['recall']('secret')}")
    print(f"Recall 'unknown': {v['recall']('unknown')}")


if __name__ == "__main__":
    main()
