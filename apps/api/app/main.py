from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.api.app.routes.predictions import router as predictions_router

app = FastAPI(title="Race Predictions AI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predictions_router, prefix="/predictions", tags=["predictions"])


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "service": "pitwall-ai"}