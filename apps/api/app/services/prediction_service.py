from typing import Literal

from apps.api.app.schemas.prediction import DriverPrediction
from f1models.baselines.average import AverageRacePredictor
from f1models.baselines.recent_form import RecentFormRacePredictor
from f1models.types import DriverBaseline

PredictionModelName = Literal["average", "recent-form"]


class PredictionService:
    def __init__(self) -> None:
        self.models = {
            "average": AverageRacePredictor(),
            "recent-form": RecentFormRacePredictor(),
        }

    def get_race_predictions(
        self, model: PredictionModelName
    ) -> list[DriverPrediction]:
        predictions = self._predict(model)

        return [
            DriverPrediction(
                driver=p.driver,
                podium_probability=p.podium_probability,
                points_probability=p.points_probability,
            )
            for p in predictions
        ]

    def _predict(self, model: PredictionModelName) -> list[DriverBaseline]:
        predictor = self.models[model]
        return predictor.predict_race()
