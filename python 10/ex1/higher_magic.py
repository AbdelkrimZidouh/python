from collections.abc import Callable


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined_invocation(target: str, power: int) -> tuple[str, str]:
        return (spell1(target, power), spell2(target, power))
    return combined_invocation


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def amplified_invocation(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return amplified_invocation


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def guarded_invocation(target: str, power: int) -> str:
        if not condition(target, power):
            return "Spell fizzled"
        return spell(target, power)
    return guarded_invocation


def spell_sequence(spells: list[Callable]) -> Callable:
    def sequence_invocation(target: str, power: int) -> list[str]:
        return [f(target, power) for f in spells]
    return sequence_invocation


def cast_fire(target: str, power: int) -> str:
    return f"Fireball hits {target}"


def cast_heal(target: str, power: int) -> str:
    return f"Heals {target}"


def power_to_str(target: str, power: int) -> str:
    return str(power)


def main() -> None:
    print("\nTesting spell combiner...")
    dual_spell = spell_combiner(cast_fire, cast_heal)
    r1, r2 = dual_spell("Dragon", 10)
    print(f"Combined spell result: {r1}, {r2}")

    print("\nTesting power amplifier...")
    mega_spell = power_amplifier(power_to_str, 3)
    print(f"Original: {power_to_str('None', 10)}, "
          f"Amplified: {mega_spell('None', 10)}")


if __name__ == "__main__":
    main()
