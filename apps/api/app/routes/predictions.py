from fastapi import APIRouter

from apps.api.app.schemas.prediction import DriverPrediction
from apps.api.app.services.prediction_service import PredictionService

router = APIRouter()
service = PredictionService()


@router.get("/", response_model=list[DriverPrediction])
def get_predictions() -> list[DriverPrediction]:
    return service.get_race_predictions()