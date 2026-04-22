import functools
import time
import inspect
from collections.abc import Callable
from typing import Any


def spell_timer(func: Callable) -> Callable:
    @functools.wraps(func)
    def timing_proxy(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        t_start = time.perf_counter()
        outcome = func(*args, **kwargs)
        t_end = time.perf_counter()
        print(f"Spell completed in {t_end - t_start:.3f} seconds")
        return outcome
    return timing_proxy


def power_validator(min_power: int) -> Callable:
    def factory(func: Callable) -> Callable:
        @functools.wraps(func)
        def proxy(*args: Any, **kwargs: Any) -> Any:
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            if "power" in bound.arguments:
                actual_power = bound.arguments["power"]
            elif len(args) > 0:
                actual_power = args[0]
            else:
                actual_power = 0

            if isinstance(actual_power, int) and actual_power >= min_power:
                return func(*args, **kwargs)
            return "Insufficient power for this spell"
        return proxy
    return factory


def retry_spell(max_attempts: int) -> Callable:
    def factory(func: Callable) -> Callable:
        @functools.wraps(func)
        def proxy(*args: Any, **kwargs: Any) -> Any:
            for current_try in range(1, max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print(f"Spell failed, retrying... "
                          f"(attempt {current_try}/{max_attempts})")
            try:
                return func(*args, **kwargs)
            except Exception:
                return f"Spell casting failed after {max_attempts} attempts"
        return proxy
    return factory


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return len(name) >= 3 and name.replace(" ", "").isalpha()

    @power_validator(10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


@spell_timer
def basic_fireball() -> str:
    time.sleep(0.1)
    return "Fireball cast!"


@retry_spell(3)
def guaranteed_fail() -> str:
    raise ValueError("Always fails")


def main() -> None:
    print("Testing spell timer...")
    print(f"Result: {basic_fireball()}")

    print("\nTesting retrying spell...")
    print(guaranteed_fail())
    print("Waaaaaaagh spelled !")

    print("\nTesting MageGuild...")
    mg = MageGuild()
    print(mg.validate_mage_name("Merlin"))
    print(mg.validate_mage_name("X"))
    print(mg.cast_spell("Lightning", 15))
    print(mg.cast_spell("Lightning", 5))


if __name__ == "__main__":
    main()
