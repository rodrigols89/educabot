# app/services/message_processor_service.py

"""
Message processing service.
"""

from sqlalchemy.orm import Session

from app.repositories.gestor_repository import (
    get_gestor_by_phone,
)
from app.schemas.evolution import EvolutionMessage
from app.services.pedido_service import (
    create_request,
)


def process_message(
    db: Session,
    message: EvolutionMessage,
) -> str:
    """
    Process incoming WhatsApp message.
    """

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

    if not message.text.startswith("/"):
        return "Not a command"

    try:
        pedido = create_request(
            db=db,
            gestor=gestor,
            command=message.text,
        )

        return (
            f"Request #{pedido.id} "
            f"created successfully"
        )

    except ValueError as exc:
        return str(exc)
