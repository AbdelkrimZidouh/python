from ex0 import FlameFactory, AquaFactory
from ex0.factories import CreatureFactory


def test_factory(factory: CreatureFactory) -> None:
    if not isinstance(factory, CreatureFactory):
        raise TypeError(
            f"Expected a CreatureFactory, but got "
            f"{type(factory).__name__}"
        )

    print("Testing factory")
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())


def test_battle(factory1: CreatureFactory, factory2: CreatureFactory) -> None:
    if not isinstance(factory1, CreatureFactory):
        raise TypeError(
            f"Expected factory1 to be a CreatureFactory, "
            f"but got {type(factory1).__name__}"
        )

    if not isinstance(factory2, CreatureFactory):
        raise TypeError(
            f"Expected factory2 to be a CreatureFactory, "
            f"but got {type(factory2).__name__}"
        )
    print("Testing battle")
    c1 = factory1.create_base()
    c2 = factory2.create_base()
    print(c1.describe())
    print(" vs.")
    print(c2.describe())
    print(" fight!")
    print(c1.attack())
    print(c2.attack())


if __name__ == "__main__":
    flame_factory = FlameFactory()
    aqua_factory = AquaFactory()

    test_factory(flame_factory)
    print()
    test_factory(aqua_factory)
    print()
    test_battle(flame_factory, aqua_factory)
