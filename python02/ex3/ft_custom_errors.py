#!/usr/bin/env python3

class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message: str = "Unknown watering error") -> None:
        super().__init__(message)


def check_plant() -> None:
    raise PlantError("The tomato plant is wilting!")


def check_water() -> None:
    raise WaterError("Not enough water in the tank!")


def test_custom_errors() -> None:
    print("=== Custom Garden Errors Demo ===")
    print()

    try:
        print("Testing PlantError...")
        check_plant()
    except PlantError as error:
        print(f"Caught PlantError: {error}")
    print()

    try:
        print("Testing WaterError...")
        check_water()
    except WaterError as error:
        print(f"Caught WaterError: {error}")
    print()

    print("Testing catching all garden errors...")

    try:
        check_plant()
    except GardenError as error:
        print(f"Caught GardenError: {error}")

    try:
        check_water()
    except GardenError as error:
        print(f"Caught GardenError: {error}")
    print()

    print("All custom error types work correctly!")


if __name__ == "__main__":
    test_custom_errors()
