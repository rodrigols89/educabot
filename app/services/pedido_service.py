# app/services/pedido_service.py

from sqlalchemy.orm import Session

from app.models.gestor import Gestor
from app.models.pedido import Pedido, TipoPedido
from app.repositories.pedido_repository import (
    create_pedido,
    get_today_pedido,
)


def save_request(
    db: Session,
    gestor: Gestor,
    command: str,
) -> tuple[Pedido | None, TipoPedido]:

    request_type = command.replace("/", "").upper()
    tipo = TipoPedido[request_type]

    existing_request = get_today_pedido(
        db=db,
        gestor_id=gestor.id,
        tipo=tipo,
    )

    # 🚫 já existe pedido dessa categoria hoje
    if existing_request:
        return None, tipo

    pedido = Pedido(
        gestor_id=gestor.id,
        tipo=tipo,
    )

    created = create_pedido(
        db=db,
        pedido=pedido,
    )

    return created, tipo
