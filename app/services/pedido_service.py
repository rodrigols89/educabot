# app/services/pedido_service.py

"""
Resumo do módulo:
Fornece serviços responsáveis pela criação e validação de
pedidos no sistema.

Descrição estendida:
Este módulo implementa a lógica de negócio para criação de
pedidos a partir dos comandos recebidos pela aplicação.

Antes de criar um pedido, o serviço verifica se o responsável
já realizou um pedido da mesma categoria no dia atual,
evitando solicitações duplicadas.

Responsabilidades principais:
- Converter comandos em tipos de pedido
- Validar pedidos duplicados no dia atual
- Criar novos pedidos quando permitido
- Registrar informações de depuração

Componentes principais:
- create_order

Dependências:
- sqlalchemy.orm.Session
- app.models.pedido.Pedido
- app.models.pedido.TipoPedido
- app.models.responsavel.Responsavel
- app.repositories.pedido_repository

Efeitos colaterais:
- Executa consultas no banco de dados
- Pode persistir novos pedidos
- Escreve informações de depuração na saída padrão

Entrada/Saída:
- Entrada: sessão ORM, responsável e comando recebido
- Saída: pedido criado (ou None) e o tipo do pedido

Estratégia de tratamento de erros:
- Não realiza tratamento explícito de exceções
- Erros do ORM são propagados ao chamador
- Utiliza None para indicar pedidos duplicados

Considerações de performance:
- Executa uma consulta antes da criação do pedido
- Evita inserções desnecessárias quando já existe pedido no dia

Notas de concorrência:
- Depende do gerenciamento da sessão SQLAlchemy
- Pode haver condição de corrida sem restrições adicionais no
  banco de dados

Exemplo de uso:
pedido, tipo = create_order(
    db=session,
    responsavel=responsavel,
    command="GAS"
)

Limitações:
- Não valida permissões do responsável
- Não trata concorrência entre requisições simultâneas

Versão/manutenção:
- Novas regras de criação de pedidos devem ser implementadas
  nesta camada de serviço.
"""

from sqlalchemy.orm import Session

from app.models.pedido import Pedido, TipoPedido
from app.models.responsavel import Responsavel
from app.repositories.pedido_repository import (
    create_pedido,
    get_today_pedido,
)


def create_order(
    db: Session,
    responsavel: Responsavel,
    command: str,
) -> tuple[Pedido | None, TipoPedido]:
    """
    Cria um pedido a partir de um comando recebido.

    Args:
        db (Session):
            Sessão ativa do SQLAlchemy utilizada para consultas
            e persistência.

        responsavel (Responsavel):
            Responsável que realizou a solicitação.

        command (str):
            Comando recebido contendo o tipo do pedido, como
            "GAS" ou "AGUA".

    Returns:
        tuple[Pedido | None, TipoPedido]:
            Tupla contendo:

            - O pedido criado quando a operação for bem-sucedida.
            - None quando já existir um pedido da mesma categoria
              no dia atual.
            - O tipo do pedido identificado.

    Raises:
        KeyError:
            Pode ocorrer caso o comando não corresponda a um
            valor válido de TipoPedido.

        sqlalchemy.exc.SQLAlchemyError:
            Pode ser propagada durante consultas ou persistência.

    Observações:
        O comando é convertido para letras maiúsculas antes da
        conversão para o enum TipoPedido.

    Efeitos colaterais:
        - Executa consultas no banco de dados.
        - Pode criar um novo registro de pedido.
        - Pode executar commit por meio do repositório.
        - Escreve informações de depuração na saída padrão.

    Exemplos:
        pedido, tipo = create_order(
            db=session,
            responsavel=responsavel,
            command="GAS"
        )

        pedido, tipo = create_order(
            db=session,
            responsavel=responsavel,
            command="AGUA"
        )

        if pedido is None:
            print("Pedido já realizado hoje")

    Avisos:
        A função pressupõe que o comando já foi validado pela
        camada responsável pela validação.

    Limitações:
        A verificação de duplicidade ocorre apenas por consulta
        prévia e não substitui restrições de unicidade no banco
        de dados.
    """

    print("\nCREATE ORDER PROCESS:")

    request_type = command.upper()
    tipo = TipoPedido[request_type]

    existing_request = get_today_pedido(
        db=db,
        responsavel_id=responsavel.id,
        tipo=tipo,
    )

    # 🚫 Já existe um pedido dessa categoria hoje
    if existing_request:
        print(
            f"Você já fez um pedido dessa categoria ({tipo}) hoje."
        )
        return None, tipo

    pedido = Pedido(
        responsavel_id=responsavel.id,
        tipo=tipo,
    )

    pedido = create_pedido(
        db=db,
        pedido=pedido,
    )

    print(f"Pedido ({tipo}) criado com sucesso!")

    return pedido, tipo
