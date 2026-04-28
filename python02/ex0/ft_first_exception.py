#!/usr/bin/env python3

def input_temperature(temp_str: str) -> int:
    return int(temp_str)


def test_temperature() -> None:
    print("=== Garden Temperature ===")
    print()
    print("Input data is '25'")
    try:
        temp: int = input_temperature("25")
    except Exception as error:
        print(f"Caught input_temperature error: {error}")
    else:
        print(f"Temperature is now {temp}°C")
    print()
    print("Input data is 'abc'")
    try:
        temp = input_temperature("abc")
    except Exception as error:
        print(f"Caught input_temperature error: {error}")
    else:
        print(f"Temperature is now {temp}°C")
    print()
    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()
