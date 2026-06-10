# app/api/webhook.py
"""
Evolution webhook endpoints.

Receives webhook events from Evolution API.
"""

from typing import Any

from fastapi import APIRouter, Request

from app.db.session import SessionLocal
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


def print_processor_result(
    result: str,
) -> None:
    """
    Print processor result.
    """

    print(
        "\n========================================"
    )
    print("PROCESSOR RESULT")
    print("========================================")
    print(result)
    print(
        "========================================\n"
    )


def process_webhook_message(
    message: Any,
) -> str:
    """
    Process incoming message.
    """

    db = SessionLocal()

    try:
        return process_message(
            db=db,
            message=message,
        )
    finally:
        db.close()


def print_webhook_error(
    exc: Exception,
) -> None:
    """
    Print webhook error.
    """

    print(
        "\n========================================"
    )
    print("WEBHOOK ERROR")
    print("========================================")
    print(exc)
    print(
        "========================================\n"
    )


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

    print(
        "\n========================================"
    )
    print("EVOLUTION PAYLOAD")
    print("========================================")
    print(payload)
    print(
        "========================================\n"
    )

    try:
        message = parse_evolution_message(
            payload
        )

        # Ignore messages sent by ourselves
        if message is None:
            return {
                "status": "ignored"
            }

        result: str = process_webhook_message(
            message
        )

        print_processor_result(
            result
        )

    except Exception as exc:
        print_webhook_error(exc)

    return {
        "status": "received"
    }
