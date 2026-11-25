from output import save_results


def test_save_results(tmp_path):
    results = ["80/tcp → open", "443/tcp → closed"]
    filename = tmp_path / "results.txt"

    save_results(results, filename)

    assert filename.read_text(encoding="utf-8") == ("80/tcp → open\n443/tcp → closed\n")


def test_save_results_overwrite(tmp_path):
    filename = tmp_path / "results.txt"
    filename.write_text("old content", encoding="utf-8")

    save_results(["80/tcp → open"], filename)

    assert filename.read_text(encoding="utf-8") == "80/tcp → open\n"
