from f1models.baselines.average import AverageRacePredictor


def test_average_predictor_returns_predictions() -> None:
    model = AverageRacePredictor()

    predictions = model.predict_race()

    assert len(predictions) > 0
    assert predictions[0].podium_probability >= 0