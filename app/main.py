"""
Main entrypoint for FastAPI application.

Initializes the API server and routes.
"""

from fastapi import FastAPI

from app.api.gestores import router as gestores_router
from app.api.health import router as health_router

app = FastAPI(
    title="WhatsApp Orders API",
    version="1.0.0",
)


app.include_router(gestores_router)
# app.include_router(pedidos_router)
# app.include_router(dashboard_router)
app.include_router(health_router)
