# ruff: noqa: PLW0717
# app/api/webhook.py

from typing import Any

from fastapi import APIRouter, Request

from app.db.session import SessionLocal
from app.models.pedido import TipoPedido
from app.services.command_service import is_valid_command
from app.services.evolution_client import send_whatsapp_message
from app.services.notification_service import build_supplier_message
from app.services.pedido_service import create_order
from app.services.responsavel_service import check_responsavel
from app.utils.evolution_parser import parse_evolution_message
from app.utils.logger import print_separator

router = APIRouter(
    prefix="/webhook",
    tags=["Webhook"],
)


@router.post("/evolution")
async def evolution_webhook(
    request: Request,
) -> dict[str, str]:

    print("\n")
    print_separator()

    payload: dict[str, Any] = await request.json()

    phone, text = parse_evolution_message(payload=payload)

    is_command = is_valid_command(text=text)

    if not is_command:
        print_separator()
        return {"status": "received"}

    session = SessionLocal()

    try:
        responsavel = check_responsavel(
            db=session,
            phone=phone,
        )

        if responsavel is None:
            print_separator()
            return {"status": "received"}

        pedido, tipo = create_order(
            db=session,
            responsavel=responsavel,
            command=text,
        )

        if pedido is None:
            tipo_nome = (
                "gás" if tipo == TipoPedido.GAS else "água"
            )

            message = (
                f"⚠️ Você já fez um pedido de {tipo_nome} hoje.\n"
                "Por favor, aguarde o atendimento do seu pedido atual."
            )

            send_whatsapp_message(
                phone=phone,
                message=message,
            )
            print_separator()
            return {"status": "received"}

        supplier_phone, message = build_supplier_message(
            responsavel=responsavel,
            tipo=pedido.tipo,
        )

        sent = send_whatsapp_message(
            phone=supplier_phone,
            message=message,
        )

        print("SUPPLIER MSG CHEKING:")

        if sent:

            print("Mensagem enviada ao forncedor com sucesso!")

            confirmation_message = (
                "✅ Seu pedido foi realizado com sucesso!"
            )

            send_whatsapp_message(
                phone=phone,
                message=confirmation_message,
            )

        else:

            print("Não foi possível enviar sua mensagem ao fornecedor.")

            unconfirmation_message = (
                "Não foi possível enviar sua mensagem ao fornecedor.\n"
                "Por favor, entre em contato com Rodrigo."
            )

            send_whatsapp_message(
                phone=phone,
                message=unconfirmation_message,
            )

    finally:
        session.close()

    print_separator()

    return {"status": "received"}
