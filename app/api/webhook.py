"""
Evolution webhook endpoints.

Receives webhook events from Evolution API.
"""

from typing import Any

from fastapi import APIRouter, Request

from app.schemas.evolution import EvolutionMessage
from app.utils.evolution_parser import (
    parse_evolution_message,
)

router = APIRouter(
    prefix="/webhook",
    tags=["Webhook"],
)


def _log_message(
    message: EvolutionMessage,
) -> None:
    """
    Log normalized Evolution message.

    Parameters
    ----------
    message : EvolutionMessage
        Parsed webhook message.

    Returns
    -------
    None

    Examples
    --------
    >>> _log_message(message)
    """
    print("\n=== EVOLUTION MESSAGE ===")
    print(f"Phone: {message.phone}")
    print(f"Name: {message.name}")
    print(f"Text: {message.text}")
    print(f"Type: {message.message_type}")
    print(f"From Me: {message.from_me}")
    print(f"Timestamp: {message.timestamp}")
    print("=========================\n")


@router.post("/evolution")
async def evolution_webhook(
    request: Request,
) -> dict[str, str]:
    """
    Receive Evolution webhook events.

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
    payload: dict[str, Any] = await request.json()

    try:
        message = parse_evolution_message(payload)
        _log_message(message)

    except Exception as exc:
        print("\n=== EVOLUTION PARSE ERROR ===")
        print(exc)
        print(payload)
        print("============================\n")

    return {"status": "received"}
