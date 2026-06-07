from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class DriverBaseline:
    driver: str
    podium_probability: float
    points_probability: float


class AverageRacePredictor:
    def __init__(self, data_path: str | Path = "data/processed/results.csv") -> None:
        self.data_path = Path(data_path)

    def predict_race(self) -> list[DriverBaseline]:
        df = pd.read_csv(self.data_path)

        rows: list[DriverBaseline] = []

        for driver, group in df.groupby("driver"):
            podium_probability = (group["finish_position"] <= 3).mean()
            points_probability = (group["points"] > 0).mean()

            rows.append(
                DriverBaseline(
                    driver=driver,
                    podium_probability=float(podium_probability),
                    points_probability=float(points_probability),
                )
            )

        return sorted(rows, key=lambda row: row.podium_probability, reverse=True)