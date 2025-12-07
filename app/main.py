# app/main.py
from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}
