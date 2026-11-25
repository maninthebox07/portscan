def save_results(results, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for result in results:
            file.write(f"{result}\n")
