# app/models/pedido.py

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
)

from app.db.base import Base


class TipoPedido(str, Enum):

    GAS = "GAS"
    AGUA = "AGUA"


class Pedido(Base):

    __tablename__ = "pedidos"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    gestor_id = Column(
        Integer,
        ForeignKey("gestores.id"),
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
