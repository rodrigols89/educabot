"""
Main entrypoint for FastAPI application.

Initializes the API server and routes.
"""

from fastapi import FastAPI

from app.api.health import router as health_router

app = FastAPI(
    title="WhatsApp Orders API",
    version="1.0.0",
)


app.include_router(health_router)
