#!/usr/bin/env python3


class Plant:
    """A class representing a plant in the garden."""
    def __init__(self) -> None:
        """Initialize a plant with default values."""
        self.name: str = ""
        self.height: int = 0
        self.age: int = 0

    def show(self) -> None:
        """Display the plant's information."""
        print(f"{self.name}: {self.height}cm, {self.age} days old")


def main() -> None:
    """Create several plant instances and display their information."""
    rose = Plant()
    rose.name = "Rose"
    rose.height = 25
    rose.age = 30

    sunflower = Plant()
    sunflower.name = "Sunflower"
    sunflower.height = 80
    sunflower.age = 45

    cactus = Plant()
    cactus.name = "Cactus"
    cactus.height = 15
    cactus.age = 120

    print("=== Garden Plant Registry ===")
    plants = [rose, sunflower, cactus]
    for plant in plants:
        plant.show()


if __name__ == "__main__":
    main()
