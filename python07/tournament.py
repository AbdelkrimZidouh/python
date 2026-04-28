from ex0 import FlameFactory, AquaFactory
from ex0.factories import CreatureFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    BattleStrategy,
    NormalStrategy,
    AggressiveStrategy,
    DefensiveStrategy,
)


def battle(
    opponents: list[tuple[CreatureFactory, BattleStrategy]]
) -> None:
    for factory, strategy in opponents:
        if not isinstance(factory, CreatureFactory):
            raise TypeError(
                f"Expected CreatureFactory, got "
                f"{type(factory).__name__}"
            )

        if not isinstance(strategy, BattleStrategy):
            raise TypeError(
                f"Expected BattleStrategy, got "
                f"{type(strategy).__name__}"
            )
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    creatures = [(f.create_base(), s) for f, s in opponents]

    for i in range(len(creatures)):
        for j in range(i + 1, len(creatures)):
            c1, s1 = creatures[i]
            c2, s2 = creatures[j]
            print("\n* Battle *")
            print(c1.describe())
            print(" vs.")
            print(c2.describe())
            print(" now fight!")
            try:
                s1.act(c1)
                s2.act(c2)
            except ValueError as e:
                print(f"Battle error, aborting tournament: {e}")
                return


if __name__ == "__main__":
    normal = NormalStrategy()
    aggressive = AggressiveStrategy()
    defensive = DefensiveStrategy()

    print("Tournament 0 (basic)")
    print(" [ (Flameling+Normal), (Healing+Defensive) ]")
    battle([
        (FlameFactory(), normal),
        (HealingCreatureFactory(), defensive),
    ])

    print("\nTournament 1 (error)")
    print(" [ (Flameling+Aggressive), (Healing+Defensive) ]")
    battle([
        (FlameFactory(), aggressive),
        (HealingCreatureFactory(), defensive),
    ])

    print("\nTournament 2 (multiple)")
    print(" [ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]")
    battle([
        (AquaFactory(), normal),
        (HealingCreatureFactory(), defensive),
        (TransformCreatureFactory(), aggressive),
    ])
