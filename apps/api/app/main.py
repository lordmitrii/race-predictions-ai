from fastapi import FastAPI
from apps.api.app.routes.predictions import router as predictions_router

app = FastAPI(title="Race Predictions AI API")
app.include_router(predictions_router, prefix="/predictions", tags=["predictions"])

@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "service": "race-predictions-ai"}