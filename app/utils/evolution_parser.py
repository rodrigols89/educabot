"""
Evolution payload parsing utilities.
"""

from datetime import UTC, datetime
from typing import Any

from app.schemas.evolution import EvolutionMessage


def extract_message_text(
    message_data: dict[str, Any],
) -> str:
    """
    Extract text from Evolution message payload.

    Parameters
    ----------
    message_data : dict[str, Any]
        Message section from Evolution payload.

    Returns
    -------
    str
        Extracted text.
    """
    if "conversation" in message_data:
        return message_data["conversation"]

    if "extendedTextMessage" in message_data:
        return (
            message_data["extendedTextMessage"]
            .get("text", "")
        )

    return ""


def parse_evolution_message(
    payload: dict[str, Any],
) -> EvolutionMessage:
    """
    Parse Evolution webhook payload.

    Parameters
    ----------
    payload : dict[str, Any]
        Raw Evolution payload.

    Returns
    -------
    EvolutionMessage
        Normalized message object.

    Examples
    --------
    >>> message = parse_evolution_message(payload)
    >>> message.phone
    '5583999999999'
    """
    data: dict[str, Any] = payload["data"]

    sender: str = payload.get(
        "sender",
        "",
    )

    phone: str = sender.replace(
        "@s.whatsapp.net",
        "",
    )

    text: str = extract_message_text(
        data["message"]
    )

    return EvolutionMessage(
        phone=phone,
        text=text,
        name=data.get("pushName"),
        timestamp=datetime.fromtimestamp(
            data["messageTimestamp"],
            tz=UTC,
        ),
        from_me=data["key"]["fromMe"],
        message_type=data["messageType"],
    )
