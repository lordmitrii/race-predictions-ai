from dataclasses import dataclass


@dataclass
class DriverBaseline:
    driver: str
    podium_probability: float
    points_probability: float
