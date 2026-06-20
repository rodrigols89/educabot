# app/services/notification_service.py

from app.models.gestor import Gestor
from app.models.pedido import TipoPedido


SUPPLIERS = {
    TipoPedido.GAS: {
        "name": "Del",
        "phone": "558396241663",
    },
    TipoPedido.AGUA: {
        "name": "Jaelson",
        "phone": "558396241663",
    },
}


def build_supplier_message(
    gestor: Gestor,
    tipo: TipoPedido,
) -> tuple[str, str]:

    supplier = SUPPLIERS[tipo]

    if tipo == TipoPedido.GAS:
        item = "gás"
    else:
        item = "pipa"

    message = (
        f"Bom dia!\n"
        f"1 {item} para a escola "
        f"{gestor.instituicao}, "
        f"responsável {gestor.nome}, "
        f"telefone para contato "
        f"{gestor.telefone}."
    )

    return (
        supplier["phone"],
        message,
    )

"""
# driver.py

from app.models.gestor import Gestor
from app.models.pedido import TipoPedido
from app.services.notification_service import (
    build_supplier_message,
)

gestor = Gestor(
    id=1,
    nome="Sandra",
    telefone="5583999999999",
    instituicao="Escola Maria Batista",
    pode_pedir_gas=True,
    pode_pedir_agua=True,
    ativo=True,
)

supplier_phone, message = (
    build_supplier_message(
        gestor=gestor,
        tipo=TipoPedido.GAS,
    )
)

print(
    "\n========================================"
)
print("MENSAGEM PARA FORNECEDOR")
print(
    "========================================"
)
print(
    f"Fornecedor: {supplier_phone}"
)
print(
    "----------------------------------------"
)
print(message)
print(
    "========================================\n"
)
"""
