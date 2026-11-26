def save_results(results: list[str], filename: str) -> None:
    """
    Save scan results to a text file.

    Creates the file if it does not exist and overwrites it if it does.

    Args:
        results: List of scan results to save.
        filename: Destination file path.

    Raises:
        OSError: If the file cannot be created or written.
    """
    with open(filename, "w", encoding="utf-8") as file:
        for result in results:
            file.write(f"{result}\n")
