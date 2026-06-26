# app/services/pedido_service.py

"""
Resumo do módulo:
Fornece serviços responsáveis pela criação e validação de
pedidos no sistema.

Descrição estendida:
Este módulo implementa a lógica de negócio para criação de
pedidos a partir de comandos recebidos.

Antes de criar um pedido, o serviço valida se já existe um
pedido do mesmo tipo para o responsável no dia atual, evitando
duplicidades.

Responsabilidades principais:
- Interpretar comandos de criação de pedido
- Converter comandos em tipos de pedido
- Validar existência de pedidos no dia atual
- Criar novos pedidos quando permitido
- Registrar logs de execução

Componentes principais:
- create_order

Dependências:
- sqlalchemy.orm.Session
- app.models.pedido.Pedido
- app.models.pedido.TipoPedido
- app.models.responsavel.Responsavel
- app.repositories.pedido_repository

Efeitos colaterais:
- Pode persistir novos pedidos no banco de dados
- Executa consultas de validação
- Escreve logs de depuração na saída padrão

Entrada/Saída:
- Entrada: sessão ORM, responsável e comando
- Saída: tupla contendo pedido criado (ou None) e tipo

Estratégia de tratamento de erros:
- Não realiza tratamento explícito de exceções
- Erros de ORM são propagados ao chamador
- Falhas de validação retornam None

Considerações de performance:
- Executa consulta prévia antes de inserção
- Evita duplicação de registros por dia

Notas de concorrência:
- Depende do gerenciamento de sessão SQLAlchemy
- Pode haver condição de corrida sem bloqueios adicionais

Exemplo de uso:
pedido, tipo = create_order(
    db=session,
    responsavel=responsavel,
    command="/gas"
)

Limitações:
- Não valida permissões do responsável
- Depende da integridade do comando recebido
- Não trata concorrência entre múltiplas requisições

Versão/manutenção:
- Regras de criação de pedidos devem ser mantidas nesta
  camada de serviço.
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
            Sessão ativa do SQLAlchemy utilizada para operações
            de banco de dados.

        responsavel (Responsavel):
            Entidade responsável pela solicitação do pedido.

        command (str):
            Comando recebido pela aplicação, representando o tipo
            de pedido (ex: "/gas", "/agua").

    Returns:
        tuple[Pedido | None, TipoPedido]:
            Retorna uma tupla contendo:

            - Pedido criado quando a operação é bem-sucedida.
            - None quando já existe um pedido do mesmo tipo no dia.
            - TipoPedido correspondente ao comando processado.

    Raises:
        KeyError:
            Pode ocorrer caso o comando não corresponda a um valor
            válido do enum TipoPedido.

        sqlalchemy.exc.SQLAlchemyError:
            Pode ser propagada durante consulta ou persistência.

    Observações:
        O comando é normalizado removendo "/" e convertido para
        maiúsculas antes da conversão para enum.

    Efeitos colaterais:
        - Consulta o banco de dados para validação.
        - Pode inserir um novo registro de pedido.
        - Pode executar commit via repositório.

    Exemplos:
        pedido, tipo = create_order(
            db=session,
            responsavel=responsavel,
            command="/gas"
        )

        pedido, tipo = create_order(
            db=session,
            responsavel=responsavel,
            command="/agua"
        )

        if pedido is None:
            print("Pedido já realizado hoje")

    Avisos:
        A função depende da validação prévia do responsável.

    Limitações:
        Não valida permissões do responsável.
        Não trata concorrência entre múltiplas requisições.
    """

    print("\nCREATE ORDER PROCESS:")

    request_type = command.replace("/", "").upper()
    tipo = TipoPedido[request_type]

    existing_request = get_today_pedido(
        db=db,
        responsavel_id=responsavel.id,
        tipo=tipo,
    )

    # 🚫 já existe pedido dessa categoria hoje
    if existing_request:
        print(f"Você já fez um pedido dessa categoria ({tipo}) hoje.")
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
