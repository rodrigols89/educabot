# app/services/notification_service.py

"""
Resumo do módulo:
Fornece funcionalidades para geração de mensagens destinadas
a fornecedores.

Descrição estendida:
Este módulo centraliza a configuração dos fornecedores
responsáveis pelo atendimento de pedidos e a construção das
mensagens enviadas a eles.

A partir do tipo de pedido e dos dados do responsável, o
módulo gera uma mensagem formatada contendo as informações
necessárias para atendimento da solicitação.

Responsabilidades principais:
- Manter o mapeamento de fornecedores por tipo de pedido
- Gerar mensagens para fornecedores
- Definir destinatários para notificações
- Padronizar o conteúdo das solicitações

Componentes principais:
- SUPPLIERS
- build_supplier_message

Dependências:
- app.models.pedido.TipoPedido
- app.models.responsavel.Responsavel

Efeitos colaterais:
- Nenhum efeito colateral externo
- Apenas gera dados em memória

Entrada/Saída:
- Entrada: responsável e tipo de pedido
- Saída: telefone do fornecedor e mensagem formatada

Estratégia de tratamento de erros:
- Não realiza tratamento explícito de exceções
- Depende da existência do tipo de pedido no mapeamento de
  fornecedores

Considerações de performance:
- Operações simples de acesso a dicionários e formatação de
  strings
- Custo computacional desprezível

Notas de concorrência:
- Não mantém estado mutável durante execução
- Seguro para uso concorrente

Exemplo de uso:
phone, message = build_supplier_message(
    responsavel=responsavel,
    tipo=TipoPedido.GAS
)

Limitações:
- Fornecedores são definidos estaticamente no código
- Não suporta múltiplos fornecedores por categoria
- Não possui integração direta com serviços de envio

Versão/manutenção:
- Novos tipos de pedido exigem atualização do mapeamento
  SUPPLIERS
"""

from app.models.pedido import TipoPedido
from app.models.responsavel import Responsavel

SUPPLIERS = {
    TipoPedido.GAS: {
        "name": "Del",
        "phone": "5517981471335",
    },
    TipoPedido.AGUA: {
        "name": "Jaelson",
        "phone": "5517981471335",
    },
}


def build_supplier_message(
    responsavel: Responsavel,
    tipo: TipoPedido,
) -> tuple[str, str]:
    """
    Gera a mensagem destinada ao fornecedor responsável pelo
    atendimento do pedido.

    Args:
        responsavel (Responsavel):
            Responsável que realizou a solicitação.

        tipo (TipoPedido):
            Tipo do pedido que será encaminhado ao fornecedor.

    Returns:
        tuple[str, str]:
            Tupla contendo:

            - Número de telefone do fornecedor.
            - Mensagem formatada para envio.

    Raises:
        KeyError:
            Pode ocorrer caso o tipo informado não esteja
            configurado no mapeamento de fornecedores.

    Observações:
        O conteúdo da mensagem varia conforme o tipo de pedido.

        Para pedidos de gás, a mensagem solicita uma unidade de
        gás.

        Para pedidos de água, a mensagem solicita um pipa.

    Efeitos colaterais:
        Nenhum.

    Exemplos:
        phone, message = build_supplier_message(
            responsavel=responsavel,
            tipo=TipoPedido.GAS
        )

        phone, message = build_supplier_message(
            responsavel=responsavel,
            tipo=TipoPedido.AGUA
        )

        print(phone)
        print(message)

    Avisos:
        O fornecedor deve estar previamente cadastrado no
        mapeamento SUPPLIERS.

    Limitações:
        Não realiza envio da mensagem.
        Não valida dados do responsável.
        Utiliza fornecedores definidos estaticamente.
    """

    print("\nCHOOSE SUPPLIER/MESSAGE PROCESS:")

    supplier = SUPPLIERS[tipo]

    if tipo == TipoPedido.GAS:
        item = "gás"
    else:
        item = "pipa"

    message = (
        f"Bom dia!\n"
        f"1 {item} para "
        f"{responsavel.instituicao}, "
        f"responsável pelo pedido {responsavel.nome}, "
        f"telefone para contato "
        f"{responsavel.telefone}."
    )

    print(
        f"Pedido de {item} será enviado para "
        f"{supplier['name']} ({supplier['phone']})"
    )

    print(
        f"Mensagem enviada:\n"
        f"{message}"
    )

    return (
        supplier["phone"],
        message,
    )
