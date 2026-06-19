# app/api/webhook.py

from typing import Any

from fastapi import APIRouter, Request

from app.db.session import SessionLocal
from app.services.command_service import (
    is_valid_command,
)
from app.services.gestor_service import (
    find_gestor,
)
from app.services.pedido_service import (
    save_request,
)
from app.utils.evolution_parser import (
    parse_evolution_message,
)

router = APIRouter(
    prefix="/webhook",
    tags=["Webhook"],
)


@router.post("/evolution")
async def evolution_webhook(
    request: Request,
) -> dict[str, str]:

    payload: dict[str, Any] = (
        await request.json()
    )

    phone, text = parse_evolution_message(
        payload
    )

    is_command: bool = is_valid_command(
        phone=phone,
        text=text,
    )

    if not is_command:

        print(
            "COMANDO INVÁLIDO OU IGNORADO"
        )
        print(
            "========================================\n"
        )

        return {
            "status": "received"
        }

    db = SessionLocal()

    try:

        gestor = find_gestor(
            db=db,
            phone=phone,
        )

        if gestor is None:

            print(
                "RESPONSÁVEL PELO PEDIDO NÃO ENCONTRADO"
            )
            print(
                f"Telefone: {phone}"
            )
            print(
                "========================================\n"
            )

            return {
                "status": "received"
            }

        print(
            "RESPONSÁVEL PELO PEDIDO ENCONTRADO"
        )
        print(
            f"Nome: {gestor.nome}"
        )
        print(
            f"Telefone: {gestor.telefone}"
        )
        print(
            f"Instituição: {gestor.instituicao}"
        )

        pedido = save_request(
            db=db,
            gestor=gestor,
            command=text,
        )

        if pedido is None:

            print(
                "\nPEDIDO JÁ REALIZADO HOJE"
            )
            print(
                f"Gestor: {gestor.nome}"
            )
            print(
                f"Tipo: {text}"
            )

        else:

            print(
                "\nPEDIDO SALVO"
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

    return {
        "status": "received"
    }
