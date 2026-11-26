def save_results(results: list[str], filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        for result in results:
            file.write(f"{result}\n")
