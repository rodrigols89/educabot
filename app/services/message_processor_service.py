# app/services/message_processor_service.py
"""
Message processing service.

Handles incoming WhatsApp messages and
routes them to business rules.
"""

from sqlalchemy.orm import Session

from app.repositories.gestor_repository import (
    get_gestor_by_phone,
)
from app.schemas.evolution import EvolutionMessage


def process_message(
    db: Session,
    message: EvolutionMessage,
) -> str:
    """
    Process incoming WhatsApp message.

    Parameters
    ----------
    db : Session
        Database session.

    message : EvolutionMessage
        Parsed Evolution message.

    Returns
    -------
    str
        Processing result message.

    Examples
    --------
    >>> process_message(db, message)
    'Command received'
    """

    # Ignore messages sent by ourselves
    if message.from_me:
        return "Ignored own message"

    # Ignore empty messages
    if not message.text:
        return "Empty message"

    gestor = get_gestor_by_phone(
        db=db,
        phone=message.phone,
    )

    if gestor is None:
        return (
            "Phone number not registered "
            "in the system"
        )

    # Command detection
    if message.text.startswith("/"):
        return (
            f"Command received from "
            f"{gestor.nome}"
        )

    return "Not a command"
