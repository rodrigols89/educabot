"""
Healthcheck endpoint module.
Used to verify if the API is running correctly.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    """
    Health check endpoint.

    Returns
    -------
    dict
        API status confirmation.

    Examples
    --------
    >>> GET /health
    {"status": "ok"}
    """
    return {"status": "ok"}
