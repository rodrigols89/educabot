"""
Pedido model module.

This module defines the database model responsible for storing
requests made by managers.
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship

from app.db.base import Base


class RequestType(str, Enum):
    """
    Supported request categories.

    Attributes
    ----------
    GAS : str
        Gas request category.

    AGUA : str
        Water request category.
    """

    GAS = "gas"
    AGUA = "agua"


class Pedido(Base):
    """
    Request database model.

    Stores all requests performed by managers.

    Attributes
    ----------
    id : int
        Primary key identifier.

    gestor_id : int
        Associated manager identifier.

    tipo : RequestType
        Request category.

    quantidade : int
        Requested quantity.

    criado_em : datetime
        Request creation timestamp.
    """

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
        SqlEnum(RequestType),
        nullable=False,
    )

    quantidade = Column(
        Integer,
        nullable=False,
    )

    criado_em = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # Relationship with manager.
    gestor = relationship("Gestor")
