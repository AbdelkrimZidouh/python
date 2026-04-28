#!/usr/bin/env python3

import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        user_input = input(
            "Enter new coordinates as floats in format 'x,y,z': "
        )
        parts = user_input.split(",")

        if len(parts) != 3:
            print("Invalid syntax")
            continue

        try:
            x = float(parts[0].strip())
            y = float(parts[1].strip())
            z = float(parts[2].strip())
        except ValueError as error:
            wrong_value = ""
            for part in parts:
                try:
                    float(part.strip())
                except ValueError:
                    wrong_value = part.strip()
                    break
            print(f"Error on parameter '{wrong_value}': {error}")
            continue

        return (x, y, z)


def distance_to_center(position: tuple[float, float, float]) -> float:
    x, y, z = position
    return math.sqrt(x ** 2 + y ** 2 + z ** 2)


def distance_between_points(
    pos1: tuple[float, float, float],
    pos2: tuple[float, float, float]
) -> float:
    return math.sqrt(
        (pos2[0] - pos1[0]) ** 2 +
        (pos2[1] - pos1[1]) ** 2 +
        (pos2[2] - pos1[2]) ** 2
    )


def main() -> None:
    print("=== Game Coordinate System ===")
    print()

    print("Get a first set of coordinates")
    first_pos = get_player_pos()
    print(f"Got a first tuple: {first_pos}")
    print(
        f"It includes: X={first_pos[0]}, "
        f"Y={first_pos[1]}, Z={first_pos[2]}"
    )
    print(f"Distance to center: {round(distance_to_center(first_pos), 4)}")
    print()

    print("Get a second set of coordinates")
    second_pos = get_player_pos()
    dist = round(distance_between_points(first_pos, second_pos), 4)
    print(f"Distance between the 2 sets of coordinates: {dist}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
