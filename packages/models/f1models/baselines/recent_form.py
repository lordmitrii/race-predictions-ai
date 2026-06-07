from pathlib import Path

import pandas as pd

from f1models.types import DriverBaseline


class RecentFormRacePredictor:
    def __init__(
        self,
        data_path: str | Path = "data/processed/results.csv",
        window_size: int = 10,
    ) -> None:
        if window_size <= 0:
            raise ValueError("window_size must be greater than zero")

        self.data_path = Path(data_path)
        self.window_size = window_size

    def predict_race(self) -> list[DriverBaseline]:
        df = pd.read_csv(self.data_path)
        df = df.sort_values(["season", "round"])

        rows: list[DriverBaseline] = []

        for driver, group in df.groupby("driver"):
            recent_results = group.tail(self.window_size)
            podium_probability = recent_results["podium"].mean()
            points_probability = recent_results["points_finish"].mean()

            rows.append(
                DriverBaseline(
                    driver=driver,
                    podium_probability=float(podium_probability),
                    points_probability=float(points_probability),
                )
            )

        return sorted(rows, key=lambda row: row.podium_probability, reverse=True)
