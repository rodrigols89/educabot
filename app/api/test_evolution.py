"""
Evolution API test endpoints.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from app.clients.evolution_client import (
    send_text_message,
)

router = APIRouter(
    prefix="/test",
    tags=["Test"],
)


class SendMessageRequest(BaseModel):
    """
    Send message request schema.

    Attributes
    ----------
    phone : str
        Destination phone number.

    text : str
        Message content.
    """

    phone: str
    text: str


@router.post("/send-message")
def test_send_message(
    payload: SendMessageRequest,
) -> dict:
    """
    Send WhatsApp test message.

    Parameters
    ----------
    payload : SendMessageRequest
        Request payload.

    Returns
    -------
    dict
        Evolution API response.

    Examples
    --------
    >>> POST /test/send-message
    """
    return send_text_message(
        phone=payload.phone,
        text=payload.text,
    )
