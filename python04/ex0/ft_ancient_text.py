import sys
import typing


def read_file(filename: str) -> None:
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{filename}'")
    file: typing.Optional[typing.IO[str]] = None
    try:
        file = open(filename, "r")
        content: str = file.read()
        print("---\n")
        print(content, end="")
        print("\n---")
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        return
    finally:
        if file is not None:
            file.close()
            print(f"File '{filename}' closed.")


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print(f"Usage: {sys.argv[0]} <file>\n")
            sys.exit(1)
        read_file(sys.argv[1])
    except Exception as e:
        print(f"Error found: {e}")
