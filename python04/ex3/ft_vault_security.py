def secure_archive(
    filename: str,
    mode: str = "read",
    content: str = ""
) -> tuple:
    try:
        if mode == "read":
            with open(filename, "r") as f:
                data: str = f.read()
            return (True, data)
        elif mode == "write":
            with open(filename, "w") as f:
                f.write(content)
            return (True, "Content successfully written to file")
        else:
            return (False, "Invalid mode. Use 'read' or 'write'")
    except OSError as e:
        return (False, str(e))


if __name__ == "__main__":
    print("=== Cyber Archives Security ===")

    print("\nUsing 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file"))

    print("\nUsing 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("/etc/master.passwd"))

    print("\nUsing 'secure_archive' to read from a regular file:")
    result: tuple = secure_archive("ancient_fragment.txt", "delete")
    print(result)

    print("\nUsing 'secure_archive' to write previous content to a new file:")
    if result[0]:
        print(secure_archive("new_vault_fragment.txt", "write", result[1]))
