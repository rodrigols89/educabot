"""
Main entrypoint for FastAPI application.

Initializes the API server and routes.
"""

from fastapi import FastAPI

from app.api.webhook import router as webhook_router

app = FastAPI(
    title="WhatsApp Orders API",
    version="1.0.0",
)

app.include_router(webhook_router)
