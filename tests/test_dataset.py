from pathlib import Path

import pandas as pd


def test_processed_results_exists() -> None:
    path = Path("data/processed/results.csv")

    assert path.exists()


def test_processed_results_has_required_columns() -> None:
    df = pd.read_csv("data/processed/results.csv")

    required_columns = {
        "season",
        "race_name",
        "circuit",
        "driver",
        "constructor",
        "finish_position",
        "podium",
        "points_finish",
    }

    assert required_columns.issubset(df.columns)
    assert len(df) > 0