from fastapi.testclient import TestClient

from apps.api.app.main import app


client = TestClient(app)


def test_predictions_defaults_to_average_model() -> None:
    response = client.get("/predictions")

    assert response.status_code == 200
    assert len(response.json()) > 0


def test_predictions_accepts_recent_form_model() -> None:
    response = client.get("/predictions", params={"model": "recent-form"})

    assert response.status_code == 200
    assert len(response.json()) > 0
