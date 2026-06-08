"""
Evolution API client.

Provides functions for sending messages through
Evolution API.
"""

from typing import Any

import requests

from app.core.config import settings


def send_text_message(
    phone: str,
    text: str,
) -> dict[str, Any]:
    """
    Send WhatsApp text message.

    Parameters
    ----------
    phone : str
        Destination phone number.

    text : str
        Message content.

    Returns
    -------
    dict[str, Any]
        Evolution API response.

    Raises
    ------
    requests.HTTPError
        If Evolution API returns an error.

    Examples
    --------
    >>> send_text_message(
    ...     phone="5583999999999",
    ...     text="Hello"
    ... )
    """

    url: str = (
        f"{settings.EVOLUTION_API_URL}"
        f"/message/sendText/"
        f"{settings.EVOLUTION_INSTANCE}"
    )

    payload: dict[str, Any] = {
        "number": phone,
        "textMessage": {
            "text": text,
        },
    }

    headers: dict[str, str] = {
        "apikey": settings.EVOLUTION_API_KEY,
        "Content-Type": "application/json",
    }

    response = requests.post(
        url=url,
        json=payload,
        headers=headers,
        timeout=30,
    )

    print("\n=== EVOLUTION RESPONSE ===")
    print(response.status_code)
    print(response.text)
    print("==========================\n")

    response.raise_for_status()

    return response.json()
