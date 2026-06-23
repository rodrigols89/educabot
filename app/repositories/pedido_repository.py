# app/repositories/pedido_repository.py

"""
Resumo do módulo:
Fornece operações de persistência e consulta para a entidade
Pedido.

Descrição estendida:
Este módulo implementa funções de criação e busca de pedidos
no banco de dados utilizando SQLAlchemy ORM.

Ele centraliza a lógica de acesso a dados relacionada à entidade
Pedido, garantindo consistência nas operações de persistência
e consultas por critérios de negócio.

Responsabilidades principais:
- Criar novos registros de Pedido
- Consultar pedidos por data e filtros específicos
- Encapsular operações ORM da entidade Pedido

Componentes principais:
- create_pedido
- get_today_pedido

Dependências:
- datetime
- sqlalchemy.orm.Session
- app.models.pedido.Pedido
- app.models.pedido.TipoPedido

Efeitos colaterais:
- Criação, atualização e consulta de dados no banco
- Execução de commit em transações

Entrada/Saída:
- Entrada: sessão ORM e parâmetros de negócio
- Saída: instâncias de Pedido ou None

Estratégia de tratamento de erros:
- Não trata exceções explicitamente
- Erros são propagados pela camada SQLAlchemy

Considerações de performance:
- Consultas filtradas por índice de data e chave estrangeira
- Uso de intervalo de datas para reduzir varredura no banco

Notas de concorrência:
- Dependente da sessão SQLAlchemy utilizada
- Operações de escrita podem sofrer concorrência em ambientes
  multi-thread

Exemplo de uso:
pedido = Pedido(
    responsavel_id=1,
    tipo=TipoPedido.GAS
)

create_pedido(db=session, pedido=pedido)

pedido_hoje = get_today_pedido(
    db=session,
    responsavel_id=1,
    tipo=TipoPedido.GAS
)

Limitações:
- Não implementa regras de negócio
- Não valida permissões de criação
- Não gerencia transações complexas

Versão/manutenção:
- Deve evoluir junto com regras de negócio de pedidos
"""

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.pedido import Pedido, TipoPedido


def create_pedido(
    db: Session,
    pedido: Pedido,
) -> Pedido:
    """
    Cria um novo pedido no banco de dados.

    Args:
        db (Session):
            Sessão ativa do SQLAlchemy utilizada para persistência.

        pedido (Pedido):
            Instância do modelo Pedido a ser persistida.

    Returns:
        Pedido:
            Instância do pedido após persistência no banco,
            incluindo valores atualizados (como id).

    Raises:
        sqlalchemy.exc.SQLAlchemyError:
            Pode ser levantada caso ocorra erro durante commit
            ou persistência.

    Side Effects:
        - Adiciona o objeto na sessão ORM
        - Executa commit no banco de dados
        - Atualiza a instância com refresh

    Examples:
        pedido = Pedido(
            responsavel_id=1,
            tipo=TipoPedido.GAS
        )

        pedido_criado = create_pedido(
            db=session,
            pedido=pedido
        )

        print(pedido_criado.id)

    Notes:
        Esta função realiza commit imediato, portanto não faz
        parte de uma transação encadeada.

    Warnings:
        O commit automático pode impactar fluxos transacionais
        mais complexos.
    """

    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    return pedido


def get_today_pedido(
    db: Session,
    responsavel_id: int,
    tipo: TipoPedido,
) -> Pedido | None:
    """
    Busca o pedido de um responsável no dia atual.

    Args:
        db (Session):
            Sessão ativa do SQLAlchemy utilizada para consulta.

        responsavel_id (int):
            Identificador do responsável dono do pedido.

        tipo (TipoPedido):
            Tipo do pedido a ser filtrado (GAS ou AGUA).

    Returns:
        Pedido | None:
            Instância de Pedido encontrada no dia atual ou None
            caso não exista registro.

    Raises:
        sqlalchemy.exc.SQLAlchemyError:
            Pode ser levantada em caso de falha na consulta.

    Notes:
        A busca considera o intervalo completo do dia UTC,
        iniciando às 00:00:00 e finalizando antes do próximo dia.

    Side Effects:
        Executa consulta de leitura no banco de dados.

    Examples:
        pedido = get_today_pedido(
            db=session,
            responsavel_id=1,
            tipo=TipoPedido.GAS
        )

        if pedido:
            print("Pedido já existe hoje")

        pedido = get_today_pedido(
            db=session,
            responsavel_id=2,
            tipo=TipoPedido.AGUA
        )

    Warnings:
        O uso de UTC pode gerar divergência com timezone local
        dependendo da aplicação.

    Limitations:
        Retorna apenas um pedido por dia (primeiro encontrado).
    """

    start_of_day = datetime.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    end_of_day = start_of_day + timedelta(days=1)

    return (
        db.query(Pedido)
        .filter(Pedido.responsavel_id == responsavel_id)
        .filter(Pedido.tipo == tipo)
        .filter(Pedido.criado_em >= start_of_day)
        .filter(Pedido.criado_em < end_of_day)
        .first()
    )
