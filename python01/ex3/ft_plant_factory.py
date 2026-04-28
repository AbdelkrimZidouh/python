#!/usr/bin/env python3


class Plant:
    """Represents a plant with initial characteristics."""
    def __init__(self, name: str, height: float, age: int) -> None:
        """ Initialize a plant with a name, height, and age. """
        self.name: str = name
        self.height: float = height
        self.plant_age: int = age
        self.daily_growth: float = 0.8

    def show(self) -> None:
        """Display the plant's information."""
        print(f"{self.name}: {self.height:.1f}cm, {self.plant_age} days old")

    def grow(self) -> None:
        """Increase the plant's height based on daily growth."""
        self.height = round(self.height + self.daily_growth, 1)

    def age(self) -> None:
        """Increase the plant's age by one day."""
        self.plant_age += 1


def main() -> None:
    """Create multiple plants and display them."""
    plants = [
        Plant("Rose", 25.0, 30),
        Plant("Oak", 200.0, 365),
        Plant("Cactus", 5.0, 90),
        Plant("Sunflower", 80.0, 45),
        Plant("Fern", 15.0, 120),
    ]

    print("=== Plant Factory Output ===")
    for plant in plants:
        print("Created: ", end="")
        plant.show()


if __name__ == "__main__":
    main()
