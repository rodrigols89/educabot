"""
Evolution webhook endpoints.

Receives webhook events from Evolution API.
"""

from typing import Any

from fastapi import APIRouter, Request

from app.db.session import SessionLocal
from app.schemas.evolution import EvolutionMessage
from app.services.message_processor_service import (
    process_message,
)
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

    print("\n---------------------------------------------------------------")
    print("\n=== EVOLUTION MESSAGE ===")
    print(f"Phone: {message.phone}")
    print(f"Name: {message.name}")
    print(f"Text: {message.text}")
    print(f"Type: {message.message_type}")
    print(f"From Me: {message.from_me}")
    print(f"Timestamp: {message.timestamp}")


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

    db = SessionLocal()

    try:
        message = parse_evolution_message(payload)

        _log_message(message)

        result: str = process_message(
            db=db,
            message=message,
        )

        print(
            f"Processor Result: {result}"
        )

    except Exception as exc:
        print("\n=== EVOLUTION ERROR ===")
        print(exc)
        print(payload)
        print("=======================\n")

    finally:
        db.close()

    return {"status": "received"}
