# app/services/notification_service.py

"""
Resumo do módulo:
Fornece serviços para seleção de fornecedores e geração de
mensagens de solicitação.

Descrição estendida:
Este módulo centraliza as regras de negócio responsáveis por
selecionar o fornecedor adequado para cada tipo de pedido e
gerar a mensagem que será enviada via WhatsApp.

A seleção do fornecedor pode variar conforme o tipo do pedido
e a instituição do responsável.

Responsabilidades principais:
- Selecionar fornecedores conforme regras de negócio
- Aplicar regras específicas por instituição
- Gerar mensagens padronizadas para fornecedores
- Registrar informações de depuração

Componentes principais:
- SUPPLIERS
- build_supplier_message

Dependências:
- app.core.config.settings
- app.models.pedido.TipoPedido
- app.models.responsavel.Responsavel

Efeitos colaterais:
- Escreve informações de depuração na saída padrão

Entrada/Saída:
- Entrada: responsável e tipo do pedido
- Saída: telefone do fornecedor e mensagem formatada

Estratégia de tratamento de erros:
- Não realiza tratamento explícito de exceções
- Depende da existência das configurações carregadas em
  settings

Considerações de performance:
- Executa apenas operações em memória
- Não realiza acesso ao banco de dados
- Não realiza chamadas para serviços externos

Notas de concorrência:
- Não mantém estado compartilhado mutável
- Seguro para execução concorrente
- As configurações são utilizadas apenas para leitura

Exemplo de uso:
phone, message = build_supplier_message(
    responsavel=responsavel,
    tipo=TipoPedido.GAS
)

Limitações:
- Os fornecedores são definidos por configuração
- Não realiza o envio das mensagens
- As regras de seleção estão codificadas neste módulo

Versão/manutenção:
- Novas regras de seleção de fornecedores devem ser
  implementadas neste módulo.
"""

from app.core.config import settings
from app.models.pedido import TipoPedido
from app.models.responsavel import Responsavel

SUPPLIERS = {
    TipoPedido.GAS: {
        "name": settings.SUPPLIER_GAS_NAME,
        "phone": settings.SUPPLIER_GAS_PHONE,
    },
    TipoPedido.AGUA: {
        "name": settings.SUPPLIER_WATER_NAME,
        "phone": settings.SUPPLIER_WATER_PHONE,
    },
}


def build_supplier_message(
    responsavel: Responsavel,
    tipo: TipoPedido,
) -> tuple[str, str]:
    """
    Seleciona o fornecedor e gera a mensagem da solicitação.

    Args:
        responsavel (Responsavel):
            Responsável que realizou o pedido.

        tipo (TipoPedido):
            Tipo do pedido solicitado.

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
        Para pedidos de água destinados à Secretaria de
        Educação é utilizado um fornecedor específico.

        A quantidade e o item solicitado variam conforme as
        regras de negócio aplicadas.

    Efeitos colaterais:
        - Escreve informações de depuração na saída padrão.
        - Registra o fornecedor selecionado.
        - Exibe a mensagem gerada.

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
        A seleção do fornecedor depende das configurações
        definidas em settings.

    Limitações:
        Não envia mensagens.
        Não valida os dados do responsável.
        Considera a instituição "Secretaria de Educação"
        utilizando comparação textual exata.
    """

    print("\nCHOOSE SUPPLIER/MESSAGE PROCESS:")

    supplier = SUPPLIERS[tipo]

    institution = (
        responsavel.instituicao
        .strip()
        .lower()
    )

    is_secretariat_water = (
        tipo == TipoPedido.AGUA
        and institution == "secretaria de educação"
    )

    if is_secretariat_water:
        supplier = {
            "name": settings.SUPPLIER_SECRETARIAT_WATER_NAME,
            "phone": settings.SUPPLIER_SECRETARIAT_WATER_PHONE,
        }

    if tipo == TipoPedido.GAS:
        quantidade = "1"
        item = "botijão de gás"

    elif is_secretariat_water:
        quantidade = "2"
        item = "galões de água"

    else:
        quantidade = "1"
        item = "pipa d'água"

    message = (
        f"Bom dia!\n"
        f"{quantidade} {item} para a {responsavel.instituicao}, por favor.\n"
        f"Responsável pelo pedido: {responsavel.nome}.\n"
        f"Telefone para contato: {responsavel.telefone}."
    )

    print(
        f"Pedido de {quantidade} {item} será enviado para "
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
