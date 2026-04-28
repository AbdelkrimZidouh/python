#!/usr/bin/env python3

class Plant:
    """Represents a plant with protected height and age attributes."""

    def __init__(self, name: str, height: float, age: int) -> None:
        """
        Initialize a plant with a name, height, and age.

        Invalid values (negative height or age) are rejected,
        and default values are used instead.

        :param name: Name of the plant
        :param height: Initial height in centimeters
        :param age: Initial age in days
        """
        self.name: str = name
        self.daily_growth: float = 0.8
        self._height: float = 0.0
        self._age: int = 0

        if height >= 0:
            self._height = height
        else:
            print(f"{self.name}: Error, height can't be negative")

        if age >= 0:
            self._age = age
        else:
            print(f"{self.name}: Error, age can't be negative")

    def set_height(self, height: float) -> bool:
        """
        Set the plant's height if the value is valid.

        :param height: New height value
        :return: True if update succeeds, False otherwise
        """
        if height < 0:
            print(f"{self.name}: Error, height can't be negative")
            return False
        self._height = height
        return True

    def set_age(self, age: int) -> bool:
        """
        Set the plant's age if the value is valid.

        :param age: New age value
        :return: True if update succeeds, False otherwise
        """
        if age < 0:
            print(f"{self.name}: Error, age can't be negative")
            return False
        self._age = age
        return True

    def get_height(self) -> float:
        """
        Get the current height of the plant.

        :return: Current height
        """
        return self._height

    def get_age(self) -> int:
        """
        Get the current age of the plant.

        :return: Current age
        """
        return self._age

    def grow(self) -> None:
        """Increase the plant's height based on daily growth."""
        self._height = round(self._height + self.daily_growth, 1)

    def age(self) -> None:
        """Increase the plant's age by one day."""
        self._age += 1

    def show(self) -> None:
        """Display the plant's current state."""
        print(f"{self.name}: {self._height:.1f}cm, {self._age} days old")


def main() -> None:
    """
    Demonstrate the use of the Plant class with encapsulation.

    Shows:
    - valid updates
    - invalid updates (rejected)
    - final state consistency
    """
    print("=== Garden Security System ===")

    rose = Plant("Rose", 15.0, 10)
    print("Plant created: ", end="")
    rose.show()
    print("\n")

    if rose.set_height(25):
        print("Height updated: 25cm")
    else:
        print("Height update rejected")

    if rose.set_age(30):
        print("Age updated: 30 days")
    else:
        print("Age update rejected")

    print("\n")

    if rose.set_height(-5):
        print("Height updated")
    else:
        print("Height update rejected")

    if rose.set_age(-2):
        print("Age updated")
    else:
        print("Age update rejected")

    print("\n")

    print("Current state: ", end="")
    rose.show()


if __name__ == "__main__":
    main()
