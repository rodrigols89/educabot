# app/models/pedido.py

"""
Resumo do módulo:
Define o modelo ORM Pedido e a enumeração TipoPedido.

Descrição estendida:
Este módulo é responsável por representar pedidos realizados
no sistema. Ele define os tipos de pedidos permitidos e o
modelo ORM utilizado para persistir pedidos no banco de dados.

Cada pedido está associado a um responsável e possui um tipo
específico, além da data e hora de criação.

Responsabilidades principais:
- Definir os tipos válidos de pedidos
- Mapear a entidade Pedido para o banco de dados
- Estabelecer relacionamento com Responsavel
- Registrar informações de criação do pedido

Componentes principais:
- TipoPedido
- Pedido

Dependências:
- datetime
- enum
- sqlalchemy
- app.db.base.Base

Efeitos colaterais:
- Registra mapeamentos ORM no SQLAlchemy
- Contribui para a definição do schema do banco de dados

Entrada/Saída:
- Entrada: dados provenientes da aplicação e do banco
- Saída: instâncias ORM da entidade Pedido

Estratégia de tratamento de erros:
- Não realiza tratamento explícito de erros
- Depende da camada ORM e da camada de serviço

Considerações de performance:
- Utiliza índice na chave primária
- Utiliza relacionamento lazy padrão do SQLAlchemy

Notas de concorrência:
- O modelo não é thread-safe por si só
- A segurança em concorrência depende da sessão ORM utilizada

Exemplo de uso:
pedido = Pedido(
    responsavel_id=1,
    tipo=TipoPedido.GAS
)

Limitações:
- Não implementa regras de negócio
- Não realiza validações de permissões

Versão/manutenção:
- Alterações no schema devem ser refletidas nas migrations
- Mudanças em relacionamentos exigem revisão das consultas ORM
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
)
from sqlalchemy import (
    Enum as SqlEnum,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class TipoPedido(str, Enum):
    """
    Resumo da classe:
    Enumeração que define os tipos de pedidos permitidos.

    Propósito:
    Restringir os valores aceitos para o tipo de pedido,
    garantindo consistência dos dados na aplicação e no banco.

    Atributos:
        GAS (str): Representa um pedido de gás.
        AGUA (str): Representa um pedido de água.

    Visão geral dos métodos:
        Herda os comportamentos padrão da classe Enum.

    Observações:
        Os valores desta enumeração são persistidos no banco por
        meio do tipo Enum do SQLAlchemy.

    Exemplo de uso:
        tipo = TipoPedido.GAS

        if tipo == TipoPedido.AGUA:
            print("Pedido de água")

        tipo = TipoPedido("GAS")

    Notas sobre concorrência:
        Enumerações são imutáveis e seguras para uso concorrente.

    Considerações de design:
        Utiliza strings como valores para facilitar consultas,
        legibilidade e persistência no banco de dados.
    """

    GAS = "GAS"
    AGUA = "AGUA"


class Pedido(Base):
    """
    Resumo da classe:
    Modelo ORM que representa um pedido realizado no sistema.

    Propósito:
    Armazenar informações sobre solicitações de recursos,
    vinculando cada pedido a um responsável autorizado.

    Atributos:
        id (int): Identificador único do pedido.
        responsavel_id (int): Identificador do responsável.
        tipo (TipoPedido): Tipo do pedido realizado.
        criado_em (datetime): Data e hora de criação do pedido.
        responsavel (Responsavel): Responsável associado ao pedido.

    Visão geral dos métodos:
        Herda os métodos e comportamentos ORM da classe Base.

    Observações:
        O relacionamento com Responsavel utiliza backref para
        permitir acesso aos pedidos a partir do responsável.

    Exemplo de uso:
        pedido = Pedido(
            responsavel_id=1,
            tipo=TipoPedido.GAS
        )

        session.add(pedido)
        session.commit()

        pedidos = responsavel.pedidos

    Notas sobre concorrência:
        Não é thread-safe isoladamente.
        O controle de concorrência depende da sessão ORM.

    Considerações de design:
        Mantém apenas informações essenciais do pedido.
        Regras de autorização e validação devem permanecer em
        camadas superiores da aplicação.
    """

    __tablename__ = "pedidos"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    responsavel_id = Column(
        Integer,
        ForeignKey("responsavel.id"),
        nullable=False,
    )

    tipo = Column(
        SqlEnum(
            TipoPedido,
            name="tipo_pedido",
        ),
        nullable=False,
    )

    criado_em = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # Relationship with order.
    responsavel = relationship("Responsavel", backref="pedidos")
