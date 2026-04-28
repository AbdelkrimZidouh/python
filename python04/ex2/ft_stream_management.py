import sys
import typing


def read_file(filename: str) -> typing.Optional[str]:
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{filename}'")
    file: typing.Optional[typing.IO[str]] = None
    try:
        file = open(filename, "r")
        content: str = file.read()
        print("---")
        sys.stdout.write(content)
        print("\n---")
        return content
    except (OSError, UnicodeError) as e:
        sys.stderr.write(f"[STDERR] Error opening file '{filename}': {e}\n")
        sys.stderr.flush()
        return None
    finally:
        if file is not None:
            file.close()
            print(f"File '{filename}' closed.")


def transform_content(content: str) -> str:
    lines: list = content.splitlines()
    new_lines: list = [line + "#" for line in lines]
    return "\n".join(new_lines)


def save_file(filename: str, content: str) -> None:
    file: typing.Optional[typing.IO[str]] = None
    try:
        print(f"Saving data to '{filename}'")
        file = open(filename, "w")
        file.write(content)
        print(f"Data saved in file '{filename}'.")
    except OSError as e:
        sys.stderr.write(
            f"[STDERR] Error opening file '{filename}': {e}\n"
        )
        sys.stderr.flush()
        print("Data not saved.")
    finally:
        if file is not None:
            file.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        sys.exit(1)

    content: typing.Optional[str] = read_file(sys.argv[1])
    if content is None:
        sys.exit(1)

    new_content: str = transform_content(content)
    print("\nTransform data:")
    print("---")
    sys.stdout.write(new_content + "\n")
    print("---")

    sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()
    new_filename: str = sys.stdin.readline().rstrip("\n")

    if not new_filename:
        print("Not saving data.")
    else:
        save_file(new_filename, new_content)
