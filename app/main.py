# app/main.py

from fastapi import FastAPI

from app.api.webhook import router as webhook_router

app = FastAPI(
    title="EducatBot - WhatsApp Orders API",
    version="1.0.0",
)

app.include_router(webhook_router)
