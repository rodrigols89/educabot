"""
Evolution webhook endpoints.

Receives events sent by Evolution API.

Examples
--------
POST /webhook/evolution
"""

from typing import Any

from fastapi import APIRouter, Request

router = APIRouter(
    prefix="/webhook",
    tags=["Webhook"],
)


@router.post("/evolution")
async def evolution_webhook(request: Request) -> dict[str, str]:
    """
    Receive webhook events from Evolution API.

    Parameters
    ----------
    request : Request
        Incoming FastAPI request.

    Returns
    -------
    dict[str, str]
        Processing status.

    Examples
    --------
    >>> POST /webhook/evolution
    {'status': 'received'}
    """

    payload: Any = await request.json()

    print("\n=== EVOLUTION WEBHOOK ===")
    print(payload)
    print("========================\n")

    return {"status": "received"}
