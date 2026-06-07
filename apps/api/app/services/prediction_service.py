from apps.api.app.schemas.prediction import DriverPrediction
from f1models.baselines.average import AverageRacePredictor


class PredictionService:
    def __init__(self) -> None:
        self.model = AverageRacePredictor()

    def get_race_predictions(self) -> list[DriverPrediction]:
        predictions = self.model.predict_race()

        return [
            DriverPrediction(
                driver=p.driver,
                podium_probability=p.podium_probability,
                points_probability=p.points_probability,
            )
            for p in predictions
        ]