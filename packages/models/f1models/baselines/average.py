from dataclasses import dataclass


@dataclass
class DriverBaseline:
    driver: str
    podium_probability: float
    points_probability: float


class AverageRacePredictor:
    def predict_race(self) -> list[DriverBaseline]:
        return [
            DriverBaseline("Verstappen", 0.68, 0.94),
            DriverBaseline("Norris", 0.46, 0.87),
            DriverBaseline("Leclerc", 0.38, 0.82),
            DriverBaseline("Piastri", 0.34, 0.80),
        ]