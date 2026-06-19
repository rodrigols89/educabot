# app/repositories/pedido_repository.py

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.pedido import (
    Pedido,
    TipoPedido,
)


def create_pedido(
    db: Session,
    pedido: Pedido,
) -> Pedido:

    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    return pedido


def get_today_pedido(
    db: Session,
    gestor_id: int,
    tipo: TipoPedido,
) -> Pedido | None:

    today = datetime.utcnow().date()

    return (
        db.query(Pedido)
        .filter(
            Pedido.gestor_id == gestor_id
        )
        .filter(
            Pedido.tipo == tipo
        )
        .filter(
            Pedido.criado_em >= today
        )
        .first()
    )

"""
# driver.py

from app.db.session import SessionLocal
from app.repositories.gestor_repository import (
    get_gestor_by_phone,
)
from app.services.pedido_service import (
    save_request,
)

db = SessionLocal()

try:

    gestor = get_gestor_by_phone(
        db=db,
        phone="558396192515",
    )

    if gestor is None:

        print(
            "\n========================================"
        )
        print(
            "GESTOR NÃO ENCONTRADO"
        )
        print(
            "========================================"
        )
        print(
            "Telefone: 558396192515"
        )
        print(
            "========================================\n"
        )

        raise SystemExit()

    pedido = save_request(
        db=db,
        gestor=gestor,
        command="/gas",
    )

    if pedido is None:

        print(
            "\n========================================"
        )
        print(
            "PEDIDO JÁ REALIZADO HOJE"
        )
        print(
            "========================================"
        )
        print(
            f"Gestor: {gestor.nome}"
        )
        print(
            "Tipo: GAS"
        )
        print(
            "========================================\n"
        )

    else:

        print(
            "\n========================================"
        )
        print(
            "PEDIDO SALVO"
        )
        print(
            "========================================"
        )
        print(
            f"Pedido ID: {pedido.id}"
        )
        print(
            f"Gestor ID: {pedido.gestor_id}"
        )
        print(
            f"Tipo: {pedido.tipo.value}"
        )
        print(
            f"Criado em: {pedido.criado_em}"
        )
        print(
            "========================================\n"
        )

finally:
    db.close()
"""
