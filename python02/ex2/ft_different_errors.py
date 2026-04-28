#!/usr/bin/env python3

def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        result: float = 10 / 0
        print(result)
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        result = "plants: " + 5
        print(result)
    else:
        return


def test_error_types() -> None:
    print("=== Garden Error Types Demo ===")

    for operation in range(5):
        try:
            print(f"Testing operation {operation}...")
            garden_operations(operation)
            print("Operation completed successfully")
        except ValueError as error:
            print(f"Caught ValueError: {error}")
        except ZeroDivisionError as error:
            print(f"Caught ZeroDivisionError: {error}")
        except FileNotFoundError as error:
            print(f"Caught FileNotFoundError: {error}")
        except TypeError as error:
            print(f"Caught TypeError: {error}")
    print()
    print("All error types tested successfully!")


if __name__ == "__main__":
    test_error_types()
