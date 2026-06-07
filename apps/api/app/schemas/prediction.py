from pydantic import BaseModel


class DriverPrediction(BaseModel):
    driver: str
    podium_probability: float
    points_probability: float