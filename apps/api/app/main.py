from fastapi import FastAPI

app = FastAPI(title="Race Predictions AI API")


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "service": "race-predictions-ai"}