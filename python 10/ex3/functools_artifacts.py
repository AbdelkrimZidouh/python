import functools
import operator
from collections.abc import Callable
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0

    actions: dict[str, Callable[[int, int], int]] = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": lambda v1, v2: max(v1, v2),
        "min": lambda v1, v2: min(v1, v2)
    }

    if operation not in actions:
        raise ValueError(f"Unknown operation: {operation}")

    return functools.reduce(actions[operation], spells)


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    return {
        "fire": functools.partial(base_enchantment, 50, "fire"),
        "water": functools.partial(base_enchantment, 50, "water"),
        "earth": functools.partial(base_enchantment, 50, "earth")
    }


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    @functools.singledispatch
    def root_dispatcher(arg: Any) -> str:
        return "Unknown spell type"

    @root_dispatcher.register(int)
    def handle_damage(arg: int) -> str:
        return f"Damage spell: {arg} damage"

    @root_dispatcher.register(str)
    def handle_enchant(arg: str) -> str:
        return f"Enchantment: {arg}"

    @root_dispatcher.register(list)
    def handle_multi(arg: list) -> str:
        return f"Multi-cast: {len(arg)} spells"

    return root_dispatcher


def main() -> None:
    print("\nTesting spell reducer...")
    nums = [10, 20, 30, 40]
    print(f"Sum: {spell_reducer(nums, 'add')}")
    print(f"Product: {spell_reducer(nums, 'multiply')}")
    print(f"Max: {spell_reducer(nums, 'max')}")

    print("\nTesting memoized fibonacci...")
    print(f"Fib(0): {memoized_fibonacci(0)}")
    print(f"Fib(1): {memoized_fibonacci(1)}")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")

    print("\nTesting spell dispatcher...")
    sd = spell_dispatcher()
    print(sd(42))
    print(sd("fireball"))
    print(sd(["a", "b", "c"]))
    print(sd(3.14))


if __name__ == "__main__":
    main()
