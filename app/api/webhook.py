# ruff: noqa: PLW0717
# app/api/webhook.py

"""
Resumo do módulo:
Define o endpoint responsável por receber webhooks da
Evolution API e coordenar todo o fluxo de processamento dos
pedidos.

Descrição estendida:
Este módulo implementa o endpoint que recebe eventos enviados
pela Evolution API. Após receber uma mensagem, o fluxo realiza
o parsing do payload, valida o comando recebido, verifica o
responsável, cria o pedido quando permitido, seleciona o
fornecedor adequado e envia as notificações necessárias.

O endpoint sempre responde rapidamente ao webhook, retornando
uma confirmação de recebimento independentemente do resultado
do processamento interno.

Responsabilidades principais:
- Receber webhooks da Evolution API
- Interpretar mensagens recebidas
- Validar comandos enviados
- Validar responsáveis cadastrados
- Criar pedidos quando permitido
- Selecionar fornecedores
- Enviar notificações ao fornecedor
- Enviar confirmações ao responsável
- Gerenciar a sessão do banco de dados

Componentes principais:
- router
- evolution_webhook

Dependências:
- typing.Any
- fastapi
- app.db.session
- app.models.pedido
- app.services.command_service
- app.services.evolution_client
- app.services.notification_service
- app.services.pedido_service
- app.services.responsavel_service
- app.utils.evolution_parser
- app.utils.logger

Efeitos colaterais:
- Executa consultas e gravações no banco de dados
- Realiza chamadas HTTP para a Evolution API
- Escreve logs na saída padrão

Entrada/Saída:
- Entrada: requisição HTTP POST contendo o payload do webhook
- Saída: resposta JSON confirmando o recebimento do evento

Estratégia de tratamento de erros:
- Garante o fechamento da sessão do banco utilizando finally
- Não captura explicitamente exceções das camadas inferiores
- Responde ao webhook independentemente do processamento

Considerações de performance:
- Executa consultas ao banco apenas quando necessário
- Realiza chamadas síncronas para envio de mensagens
- Evita processamento de mensagens inválidas

Notas de concorrência:
- Cada requisição utiliza sua própria sessão do banco
- Seguro para execução concorrente
- Depende da concorrência suportada pelos serviços externos

Exemplo de uso:
POST /webhook/evolution

Payload:
{
    "...": "..."
}

Limitações:
- Processa apenas comandos suportados
- Depende da disponibilidade da Evolution API
- Não possui fila para processamento assíncrono

Versão/manutenção:
- Novas regras de negócio devem ser implementadas nas camadas
  de serviço, mantendo este módulo como coordenador do fluxo.
"""

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
    """
    Processa eventos enviados pela Evolution API.

    Args:
        request (Request):
            Requisição HTTP contendo o payload do webhook.

    Returns:
        dict[str, str]:
            Dicionário contendo a confirmação de recebimento do
            webhook.

            Exemplo:
                {
                    "status": "received"
                }

    Raises:
        Nenhuma exceção é tratada diretamente pela função.

        Exceções provenientes das camadas de banco de dados,
        serviços ou comunicação externa podem ser propagadas.

    Observações:
        O fluxo executado é composto pelas seguintes etapas:

        - Receber o payload.
        - Extrair telefone e mensagem.
        - Validar o comando.
        - Validar o responsável.
        - Criar o pedido.
        - Selecionar o fornecedor.
        - Enviar a solicitação ao fornecedor.
        - Informar o resultado ao responsável.

    Efeitos colaterais:
        - Executa consultas no banco de dados.
        - Pode criar novos pedidos.
        - Realiza chamadas HTTP para envio de mensagens.
        - Escreve logs na saída padrão.

    Exemplos:
        POST /webhook/evolution

        POST /webhook/evolution
        Content-Type: application/json

        {
            "...": "..."
        }

        Resposta:
        {
            "status": "received"
        }

    Avisos:
        O endpoint sempre retorna confirmação de recebimento do
        webhook, mesmo quando o processamento interno falha.

    Limitações:
        Não realiza processamento assíncrono.
        Depende dos serviços externos estarem disponíveis.
        O envio das mensagens ocorre de forma síncrona.
    """

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
