#!/usr/bin/env python3


class Plant:
    """Represents a plant with growth behavior over time."""
    def __init__(self) -> None:
        """Initialize a plant with default values."""
        self.name: str = ""
        self.height: float = 0.0
        self.plant_age: int = 0
        self.daily_growth: float = 0.8

    def show(self) -> None:
        """Display the current state of the plant."""
        print(f"{self.name}: {self.height:.1f}cm, {self.plant_age} days old")

    def grow(self) -> None:
        """Increase the plant height by its daily growth."""
        self.height = round(self.height + self.daily_growth, 1)

    def age(self) -> None:
        """Increase the plant age by one day."""
        self.plant_age += 1


def main() -> None:
    """Simulate one week of plant growth and display results."""
    rose = Plant()
    rose.name = "Rose"
    rose.height = 25.0
    rose.plant_age = 30

    start_height = rose.height

    print("=== Garden Plant Growth ===")
    for day in range(1, 8):
        print(f"=== Day {day} ===")
        rose.show()
        rose.grow()
        rose.age()

    total_growth = round(rose.height - start_height)
    print(f"Growth this week: {total_growth}cm")


if __name__ == "__main__":
    main()
