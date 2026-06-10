"""
Evolution payload parsing utilities.

Converts Evolution API payloads into
internal message objects used by the system.
"""

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

    Examples
    --------
    >>> extract_message_text(
    ...     {"conversation": "Hello"}
    ... )
    'Hello'
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
) -> EvolutionMessage | None:
    """
    Parse Evolution webhook payload.

    Parameters
    ----------
    payload : dict[str, Any]
        Raw Evolution payload.

    Returns
    -------
    EvolutionMessage | None
        Normalized message object.

    Notes
    -----
    Messages sent by the instance owner
    are ignored and return None.

    Examples
    --------
    >>> parse_evolution_message(payload)
    """

    data: dict[str, Any] = payload["data"]

    from_me: bool = data["key"]["fromMe"]

    # Ignore messages sent by ourselves
    if from_me:
        return None

    sender: str = data["key"].get(
        "senderPn",
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
    )
